import calendar
import csv
import datetime
import os

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from marketing_report.models import CustomerGroup, Customer


def customer(request):
    date_now = datetime.date.today()
    navi = 'customer'
    context = {'navi': navi, 'date_now': date_now}
    return render(request, 'customer.html', context)


def customers_current(request, date, years, search_string, id_no):
    d = datetime.datetime.strptime(date, '%Y-%m-%d')
    end_of_client = datetime.date(d.year - years, d.month, calendar.monthrange(d.year - years, d.month)[-1])
    customers = CustomerGroup.objects.filter(date_last__gte=end_of_client)
    if search_string != 'default':
        search_string = search_string.replace('_', ' ')
        customers = customers.filter(name__icontains=search_string)
    customers = list(customers.values('id', 'name', 'customer_type__name', 'business_unit__name', 'date_first', 'date_last')[
                     id_no: id_no + 50])
    return JsonResponse(customers, safe=False)


def customers_export(request):
    date = request.POST['date']
    years = request.POST['years']
    file_name = 'marketing_report/uploaded/export_cst.csv'
    d = datetime.datetime.strptime(date, '%Y-%m-%d')
    end_of_client = datetime.date(d.year - int(years), d.month, calendar.monthrange(d.year - int(years), d.month)[-1])
    customers = CustomerGroup.objects.filter(date_last__gte=end_of_client)
    try:
        if os.path.exists(file_name):
            os.remove(file_name)
        with open(file_name, 'w', newline='', encoding='utf-8') as cust_csv:
            csv_writer = csv.writer(cust_csv, delimiter=';')
            csv_writer.writerow(['Название', 'Тип', 'Первая дата', 'Последняя дата', 'Эко', ''])
            for cst in customers:
                type_name = None
                if cst.customer_type:
                    type_name = cst.customer_type.name
                csv_writer.writerow([cst.name, type_name, cst.date_first, cst.date_last, cst.business_unit, ''])
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")
        return HttpResponse("Ошибка при записи в файл", status=500)

    try:
        with open(file_name, 'rb') as file:
            response = HttpResponse(file.read(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="export_cst.csv"'
            return response
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return HttpResponse("Ошибка при чтении файла", status=500)


def show_customers_of_group(request, group_id):
    customers = Customer.objects.filter(customer_group_id=group_id)
    customers_data = list(customers.values('name', 'date_last'))
    return JsonResponse(customers_data, safe=False)
