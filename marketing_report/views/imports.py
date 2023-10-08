import csv
import datetime
import os

from django.http import JsonResponse
from django.shortcuts import render

from marketing_report.models import ImportCustomers


def imports(request):
    navi = 'imports'
    cst_date = os.path.getmtime('marketing_report/uploaded/customers.csv')
    cst_date = datetime.date.fromtimestamp(cst_date)
    customers_imported = ImportCustomers.objects.all().count()
    context = {'navi': navi, 'cst_date': cst_date, 'customers_imported': customers_imported}
    return render(request, 'import.html', context)


def import_file(request):
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
    result = (len(row) == 14)
    empty = True
    for i in range(2, len(row)):
        empty = empty and (row[i] == '' or row[i] == '0')
    return result and not empty
