import os

from datetime import datetime

from django.db.models import Min, Max
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from marketing_report.models import ImportCustomers, Customer, ReportPeriod
from marketing_report.service_functions import (cst_to_temp_db, check_new_updated, import_customer_to_customer,
                                                update_customer_from_changed, sales_to_temp_db)


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
    context = {'navi': navi, 'cst_date': cst_date, 'customers_imported': customers_imported,
               'customers_new': customers_new, 'customers_changed': customers_changed, 'sales_date': sales_date,
               'period_begin': period_begin, 'period_end': period_end}
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
        result = sales_to_temp_db()
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
    :return количество импортированных записей"""
    customers_old = Customer.objects.filter(new=True)
    customers_old = list(map(lambda customer: customer.__setattr__('new', False), customers_old))
    Customer.objects.bulk_update(customers_old, ['new'])
    customers_new = ImportCustomers.objects.filter(new=True)
    customers_new_reformatted = list(map(import_customer_to_customer, customers_new))
    result = len(customers_new_reformatted)
    if result:
        Customer.objects.bulk_create(customers_new_reformatted)
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
    return JsonResponse({'result': result})


def reassign_report_periods(request):
    begin_period = datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
    end_period = datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()
    try:
        del_periods = ReportPeriod.objects.filter(date_end__gte=begin_period, date_begin__lte=end_period)
        del_periods.delete()
    except:
        pass
    per = ReportPeriod()
    for period_type in per.calculable_list():
        per.set_period(begin_period, period_type)
        while per.date_begin < end_period:
            per.copy().save()
            per.plus(1)
    period_begin = ReportPeriod.objects.aggregate(Min('date_begin'))['date_begin__min']
    period_end = ReportPeriod.objects.aggregate(Max('date_end'))['date_end__max']
    return JsonResponse({'period_end': period_end, 'period_begin': period_begin})
