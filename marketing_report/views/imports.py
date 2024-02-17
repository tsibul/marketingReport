import os

from datetime import datetime, timedelta

from django.db.models import Min, Max, Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from marketing_report.models import ImportCustomers, Customer, ReportPeriod, SalesTransactions, CustomerGroup, \
    CustomerGroupFrigateId, RegionToFedRegion

from marketing_report.service_functions import (cst_to_temp_db, check_new_updated, import_customer_to_customer,
                                                update_customer_from_changed, sales_import_management)


def imports(request):
    navi = 'imports'
    cst_date = os.path.getmtime('marketing_report/uploaded/customers.csv')
    cst_date = datetime.fromtimestamp(cst_date).date()
    sales_date = os.path.getmtime('marketing_report/uploaded/sales.csv')
    sales_date = datetime.fromtimestamp(sales_date).date()
    customers = ImportCustomers.objects.all()
    customers_imported = customers.count()
    customers_new = customers.filter(new=True).count()
    customers_changed = customers.filter(changed=True).count()
    period_begin = ReportPeriod.objects.aggregate(Min('date_begin'))['date_begin__min']
    period_end = ReportPeriod.objects.aggregate(Max('date_end'))['date_end__max']
    import_sales = SalesTransactions.objects.all().count()
    context = {'navi': navi, 'cst_date': cst_date, 'customers_imported': customers_imported,
               'customers_new': customers_new, 'customers_changed': customers_changed, 'sales_date': sales_date,
               'period_begin': period_begin, 'period_end': period_end, 'import_sales': import_sales}
    return render(request, 'import.html', context)


def import_file(request):
    """загружает csv файл на сервер, дает ему правильное название и вызывает функцию импорта во временную БД
    :param result - количество импортированных записей """
    file_name = request.POST['file_name'] + '.csv'
    loaded_file = request.FILES['loaded_file']
    try:
        os.remove('marketing_report/uploaded/' + file_name)
    except:
        pass
    with open('marketing_report/uploaded/' + file_name, 'wb+') as destination:
        for chunk in loaded_file.chunks():
            destination.write(chunk)
    result = None
    if file_name == 'customers.csv':
        result = cst_to_temp_db()
    elif file_name == 'sales.csv':
        result = sales_import_management()
    return JsonResponse({'result': result})


def edit_temporary_base(request):
    """
    расстановка флагов 'new', 'changed' во временной базе
    :param request:
    :return:
    new_customers — количество новых клиентов в базе,
    updated_customers — количество измеененных клиентов в базе    """
    customers_list = ImportCustomers.objects.all()
    customers_list = map(check_new_updated, customers_list)
    ImportCustomers.objects.bulk_update(list(customers_list), ['new', 'changed'])
    new_customers = ImportCustomers.objects.filter(new=True).count()
    updated_customers = ImportCustomers.objects.filter(changed=True).count()
    return JsonResponse({'new_customers': new_customers, 'updated_customers': updated_customers})


def customers_new_to_main_db(request):
    """импорт новых записей из ImportCustomer в  Customer
    создание групп по умолчанию
    :return количество импортированных записей"""
    customers_old = Customer.objects.filter(new=True)
    customers_old = list(map(lambda customer: customer.__setattr__('new', False), customers_old))
    Customer.objects.bulk_update(customers_old, ['new'])
    customers_new = ImportCustomers.objects.filter(new=True)
    customers_new_reformatted = list(map(import_customer_to_customer, customers_new))
    result = len(customers_new_reformatted)
    if result:
        for customer in customers_new_reformatted:
            customer_group = CustomerGroupFrigateId.objects.filter(frigate_code=customer.frigate_code).first()
            if customer_group:
                customer.customer_group = customer_group
            else:
                customer.default_group()
        Customer.objects.bulk_create(customers_new_reformatted)
        CustomerGroup.objects.filter(customer__isnull=True, default=True).delete()
    return JsonResponse({'result': result})


def customer_change_to_customer(request):
    """ импорт измененных записей из ImportCustomer в  Customer
    :return
    :param request:
    :return: количество импортированных записей
    """
    customers_changed = ImportCustomers.objects.filter(changed=True)
    old_customer_changed = list(map(update_customer_from_changed, customers_changed))
    result = len(old_customer_changed)
    if result:
        Customer.objects.bulk_update(old_customer_changed,
                                     ['form', 'name', 'inn', 'region', 'address', 'phone', 'all_phones', 'mail',
                                      'all_mails'])

    # total_customers = Customer.objects.filter(internal=False, fed_region__isnull=True)
    # total_customers_list = []
    # groups = []
    # for customer in total_customers:
    #     fed_region = RegionToFedRegion.objects.filter(name=customer.region).first()
    #     if fed_region:
    #         customer.fed_region = fed_region.fed_region
    #         group = CustomerGroup.objects.filter(customer=customer).first()
    #         if group:
    #             if not group.fed_region:
    #                 group.fed_region = fed_region.fed_region
    #                 group.save()
    #                 groups.append(group)
    #         total_customers_list.append(customer)
    # Customer.objects.bulk_update(total_customers, ['fed_region'])
    return JsonResponse({'result': result})


def first_last_sales_dates(request):
    not_dead_customers = SalesTransactions.objects.all().values_list('customer', flat=True).distinct()
    dead_customers = Customer.objects.filter(~Q(id__in=list(not_dead_customers))).update(active=False)
    for customer_id in not_dead_customers:
        customer = Customer.objects.filter(id=customer_id).first()
        if customer:
            customer_group = customer.customer_group
            customer.active = True
            customer_group.active = True
            sales_dates = SalesTransactions.objects.filter(
                customer=customer
            ).aggregate(
                date_max=Max('sales_doc_date'),
                date_min=Min('sales_doc_date')
            )
            customer.date_first = sales_dates['date_min']
            customer.date_last = sales_dates['date_max']
            # if customer.date_last + timedelta(days=1100) >= datetime.today():
            customer.save()
            if (customer_group.date_first > customer.date_first
                    or customer_group.date_first == datetime(2000, 1, 1).date()):
                customer_group.date_first = customer.date_first
            if customer_group.date_last < customer.date_last:
                customer_group.date_last = customer.date_last
            customer_group.save()
    return HttpResponse(status=200)


def reassign_report_periods(request):
    begin_year = int(request.POST['start_date'])
    end_year = int(request.POST['end_date'])
    begin_period = datetime(begin_year, 1, 1).date()
    end_period = datetime(end_year, 12, 31).date()
    old_period_begin = ReportPeriod.objects.aggregate(Min('date_begin'))['date_begin__min']
    old_period_end = ReportPeriod.objects.aggregate(Max('date_end'))['date_end__max']
    if not old_period_begin:
        per = ReportPeriod()
        for period_type in per.calculable_list():
            per.set_period(begin_period, period_type)
            while per.date_begin < end_period:
                per.copy().save()
                per.plus(1)
    else:
        if begin_period < old_period_begin:
            per = ReportPeriod()
            for period_type in per.calculable_list():
                per.set_period(begin_period, period_type)
                while per.date_begin < old_period_begin:
                    per.copy().save()
                    per.plus(1)
        if end_period > old_period_end:
            per = ReportPeriod()
            for period_type in per.calculable_list():
                per.set_period(old_period_end + timedelta(days=1), period_type)
                while per.date_begin < end_period:
                    per.copy().save()
                    per.plus(1)
    # period_begin = ReportPeriod.objects.aggregate(Min('date_begin'))['date_begin__min']
    # period_end = ReportPeriod.objects.aggregate(Max('date_end'))['date_end__max']
    return HttpResponseRedirect(reverse('marketing_report:imports'))
    # return JsonResponse({'period_end': period_end, 'period_begin': period_begin})
