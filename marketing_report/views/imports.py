import csv
import datetime
import os

from datetime import datetime

from django.db.models import Min, Max
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from marketing_report.models import ImportCustomers, Customer, CustomerType, ReportPeriod


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


def cst_to_temp_db():
    """Импорт данных из csv файла во временную базу
    вычисляет код региона (при этом приводит коды Москвы и Московской обл к Москве, СПБ и области к СПБ,
    Крым и Севастополь к Крыму
    на запись без контактных данных и ИНН вешает флаг 'internal'
    :return result - количество импортированных записей """
    ImportCustomers.objects.all().delete()
    customers = []
    region_mapping = {
        '97': '77',
        '50': '77',
        '98': '78',
        '47': '78',
        '92': '82'
    }
    with open('marketing_report/uploaded/customers.csv', newline='', encoding='utf-8', errors='replace') as cust_csv:
        csv_reader = csv.reader(cust_csv, delimiter=';')
        for row in csv_reader:
            try:
                if customer_check_row(row):
                    (frigat_id, name, form, inn, _, address, phone, mail, comment, _, our_manager, customer_type,
                     all_mails, all_phones) = row
                    if len(inn) == 9 or len(inn) == 11:
                        inn = '0' + inn
                    region = inn[:2]
                    region = region_mapping.get(region, region)
                    internal = False
                    if (inn == '' and address == '' and phone == '' and mail == '' and comment == ''
                            and our_manager == '' and customer_type == '' and all_mails == '' and all_phones == ''):
                        internal = True
                    customer = ImportCustomers(
                        frigat_id=frigat_id,
                        name=name.replace('"', ''),
                        form=form,
                        inn=inn,
                        region=region,
                        address=address,
                        phone=phone,
                        mail=mail,
                        comment=comment,
                        our_manager=our_manager,
                        customer_type=customer_type,
                        all_mails=all_mails,
                        all_phones=all_phones,
                        internal=internal
                    )
                    customers.append(customer)
            except Exception as e:
                print(f"ошибка в записи {e}")
    result = ImportCustomers.objects.bulk_create(customers)
    return len(result)


def customer_check_row(row):
    """проверка входной строки на заполненность, то есть надо ли ее импортировать
    :return возвращает Boolean"""
    result = (len(row) == 14)
    empty = True
    for i in range(2, len(row)):
        empty = empty and (row[i] == '' or row[i] == '0')
    return result and not empty


def edit_temporary_base(request):
    """расстановка флагов 'new', 'changed' во временной базе
    :returns
    new_customers — количество новых клиентов в базе,
    updated_customers — количество измеененных клиентов в базе"""
    customers_list = ImportCustomers.objects.all()
    customers_list = map(check_new_updated, customers_list)
    ImportCustomers.objects.bulk_update(list(customers_list), ['new', 'changed'])
    new_customers = ImportCustomers.objects.filter(new=True).count()
    updated_customers = ImportCustomers.objects.filter(changed=True).count()
    return JsonResponse({'new_customers': new_customers, 'updated_customers': updated_customers})


def check_new_updated(customer: ImportCustomers):
    """проверка временной базы на наличие новых клиентов или изменения старых
    :return customer — объект с расставленными флагами"""
    old_customers_list = Customer.objects.all()
    try:
        old_customer = old_customers_list.get(frigat_id=customer.frigat_id)
        customer.new = False
        if (old_customer.name != customer.name or old_customer.inn != customer.inn or
                old_customer.address != customer.address or old_customer.mail != customer.mail or
                old_customer.all_mails != customer.all_mails or old_customer.all_phones != customer.all_phones or
                old_customer.phone != customer.phone or old_customer.form != customer.form):
            customer.changed = True
    except:
        customer.new = True
    return customer


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


def import_customer_to_customer(import_customer: ImportCustomers):
    """преобразование объекта ImportCustomer в Customer (все поля) для новых"""
    customer = Customer(
        frigat_id=import_customer.frigat_id,
        name=import_customer.name,
        form=import_customer.form,
        inn=import_customer.inn,
        region=import_customer.region,
        address=import_customer.address,
        phone=import_customer.phone,
        mail=import_customer.mail,
        comment=import_customer.comment,
        our_manager=import_customer.our_manager,
        all_mails=import_customer.all_mails,
        all_phones=import_customer.all_phones,
        internal=import_customer.internal,
        new=import_customer.new,
        date_import=datetime.date.today(),
    )
    customer_type = customer_type_choose(import_customer.customer_type, import_customer.region)
    if customer_type:
        customer.customer_type = customer_type
    return customer


def customer_type_choose(customer_type, region):
    """определение типа клиента по его названию в Фрегате"""
    if 'Конечник' in customer_type:
        type_obj = CustomerType.objects.get(
            name='Конечник Москва') if region == '77' else CustomerType.objects.get(name='Конечник Регион')
    elif 'рекламщик' in customer_type:
        type_obj = CustomerType.objects.get(
            name='Рекламщик Москва') if region == '77' else CustomerType.objects.get(name='Рекламщик Регион')
    elif 'Агентство' in customer_type:
        type_obj = CustomerType.objects.get(
            name='Агентство Москва') if region == '77' else CustomerType.objects.get(name='Агентство Регион')
    elif 'Дилер' in customer_type:
        type_obj = CustomerType.objects.get(name='Дилер Москва') if region == '77' else CustomerType.objects.get(
            name='Дилер Регион')
    elif 'точка' in customer_type:
        type_obj = CustomerType.objects.get(name='Розничная Точка')
    else:
        type_obj = ''
    return type_obj


def customer_change_to_customer(request):
    """импорт измененных записей из ImportCustomer в  Customer
    :return количество импортированных записей"""
    customers_changed = ImportCustomers.objects.filter(changed=True)
    old_customer_changed = list(map(update_customer_from_changed, customers_changed))
    result = len(old_customer_changed)
    if result:
        Customer.objects.bulk_update(old_customer_changed,
                                     ['form', 'name', 'inn', 'region', 'address', 'phone', 'all_phones', 'mail',
                                      'all_mails'])
    return JsonResponse({'result': result})


def update_customer_from_changed(customer: ImportCustomers):
    """преобразование объекта ImportCustomer в Customer для измененных"""
    new_customer = Customer.objects.get(frigat_id=customer.frigat_id)
    new_customer.name = customer.name
    new_customer.form = customer.form
    new_customer.address = customer.address
    new_customer.inn = customer.inn
    new_customer.region = customer.region
    new_customer.phone = customer.phone
    new_customer.all_phones = customer.all_phones
    new_customer.mail = customer.mail
    new_customer.all_mails = customer.all_mails
    return new_customer


def sales_to_temp_db():
    """импорт данных о продажах во временную базу"""
    result = ''
    return len(result)


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
