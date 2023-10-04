import datetime
import os

from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def imports(request):
    navi = 'imports'
    cst_date = os.path.getmtime('marketing_report/uploaded/customers.csv')
    cst_date = datetime.date.fromtimestamp(cst_date)
    context = {'navi': navi, 'cst_date': cst_date}
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
    return HttpResponseRedirect(reverse('marketing_report:imports'))
