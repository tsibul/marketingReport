import csv

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from marketing_report.models import Customer


def admin(request):
    navi = 'admin'
    # customer = Customer.objects.all().order_by('frigat_id')
    context = {'navi': navi}
    return render(request, 'admin.html', context)


def customer_export(request):
    date_last = request.POST['date_last']
    date_last = datetime.strptime(date_last, '%Y-%m-%d')
    customer = Customer.objects.filter(date_last__gte=date_last, internal=False).values_list('frigat_id', 'name',
                                                                                             'customer_type__code',
                                                                                             'customer_type__type_name')
    with open('customers.csv', 'w', newline='') as export_file:
        writer = csv.writer(export_file)
        writer.writerows(customer)
    return HttpResponseRedirect(reverse('marketing_report:admin_site'))
