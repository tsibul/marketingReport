import csv
import datetime
import os

from django.http import JsonResponse
from django.shortcuts import render
from marketing_report.models import ImportCustomers, Customer


def imports(request):
    navi = 'imports'
    cst_date = os.path.getmtime('marketing_report/uploaded/customers.csv')
    cst_date = datetime.date.fromtimestamp(cst_date)
    customers = ImportCustomers.objects.all()
    customers_imported = customers.count()
    customers_new = customers.filter(internal=False, new=True).count()
    customers_changed = customers.filter(internal=False, changed=True).count()
    context = {'navi': navi, 'cst_date': cst_date, 'customers_imported': customers_imported,
               'customers_new': customers_new, 'customers_changed': customers_changed}
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
    result = cst_to_temp_db()
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
    customers_list = ImportCustomers.objects.filter(internal=False)
    customers_list = map(check_new_updated, customers_list)
    ImportCustomers.objects.bulk_update(list(customers_list), ['new', 'changed'])
    new_customers = ImportCustomers.objects.filter(new=True, internal=False).count()
    updated_customers = ImportCustomers.objects.filter(changed=True, internal=False).count()
    return JsonResponse({'new_customers': new_customers, 'updated_customers': updated_customers})


def check_new_updated(customer):
    """проверка временной базы на наличие новых клиентов или изменения старых
    :return customer — объект с расставленными флагами"""
    old_customers_list = Customer.objects.filter(internal=False)
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
