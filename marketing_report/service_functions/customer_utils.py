import csv
from datetime import datetime

from marketing_report.models import Customer
from marketing_report.models.customer_group_models import CustomerType
from marketing_report.models.import_models import ImportCustomers


def customer_type_choose(customer_type, region):
    """
    определение типа клиента по его названию в Фрегате
    :param customer_type:
    :param region:
    :return:
    """
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
    """
    проверка входной строки на заполненность, то есть надо ли ее импортировать
    :param row: входная строка
    :return: возвращает Boolean
    """
    result = (len(row) == 14)
    empty = True
    for i in range(2, len(row)):
        empty = empty and (row[i] == '' or row[i] == '0')
    return result and not empty


def check_new_updated(customer: ImportCustomers):
    """
    проверка временной базы на наличие новых клиентов или изменения старых
    :param customer:
    :return: customer — объект с расставленными флагами
    """
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

def import_customer_to_customer(import_customer: ImportCustomers):
    """
    преобразование объекта ImportCustomer в Customer (все поля) для новых
    :param import_customer:
    :return:
    """
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
        date_import=datetime.today().date(),
    )
    customer_type = customer_type_choose(import_customer.customer_type, import_customer.region)
    if customer_type:
        customer.customer_type = customer_type
    return customer


def update_customer_from_changed(customer: ImportCustomers):
    """ преобразование объекта ImportCustomer
    в Customer для измененных
    :param customer:
    :return:
    """
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
