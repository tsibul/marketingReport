from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from marketing_report import models
from marketing_report.models import PrintType, ColorScheme, GoodCrmType, GoodMatrixType, CustomerTypes, Customer, \
    CustomerGroups, Color


def dictionary(request):
    navi = 'dictionary'
    matrix = GoodMatrixType.objects.all().order_by('matrix_name')
    crm = GoodCrmType.objects.all().order_by('crm_name')
    print_type = PrintType.objects.all().order_by('type_name')
    color_group = ColorScheme.objects.all().order_by('scheme_name')
    customer_type = CustomerTypes.objects.all().order_by('id')
    context = {'navi': navi, 'matrix': matrix, 'crm': crm, 'print_type': print_type, 'color_group': color_group,
               'customer_type': customer_type}
    return render(request, 'dictionary.html', context)


@csrf_exempt
def dictionary_update(request, dict_type):
    dict_id = request.POST['id']
    dict_model = getattr(models, dict_type)
    field_list = [f.name for f in dict_model._meta.get_fields()]
    if dict_id:
        dict_element = dict_model.objects.get(id=dict_id)
    else:
        dict_element = dict_model()
    for field in field_list:
        if field in request.POST.keys() and field != 'id':
            setattr(dict_element, field, request.POST[field])
    return HttpResponse()
