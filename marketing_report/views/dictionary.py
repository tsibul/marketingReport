import json

from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from marketing_report import models
from marketing_report.models import PrintType, ColorScheme, GoodCrmType, GoodMatrixType, CustomerTypes, Customer, \
    CustomerGroups, Color, Goods


def dictionary(request):
    navi = 'dictionary'
    matrix = GoodMatrixType.objects.all().order_by('matrix_name')
    crm = GoodCrmType.objects.all().order_by('crm_name')
    print_type = PrintType.objects.all().order_by('type_name')
    color_group = ColorScheme.objects.all().order_by('scheme_name')
    customer_type = CustomerTypes.objects.all().order_by('id')
    customer_group = CustomerGroups.objects.all().order_by('group_name')[0:19]
    customer_group_end = CustomerGroups.objects.all().order_by('group_name')[19:20]
    customer = Customer.objects.filter(internal=False).order_by('name')[0:19]
    customer_end = Customer.objects.filter(internal=False).order_by('name')[19:20]
    color = Color.objects.all().order_by('color_scheme', 'color_id')[0:19]
    color_end = Color.objects.all().order_by('color_scheme', 'color_id')[19:20]
    goods = Goods.objects.all().order_by('item_name')[0:19]
    goods_end = Goods.objects.all().order_by('item_name')[19:20]
    context = {'navi': navi, 'matrix': matrix, 'crm': crm, 'print_type': print_type, 'color_group': color_group,
               'customer_type': customer_type, 'customer_group': customer_group, 'color': color,
               'color_end': color_end, 'customer_group_end': customer_group_end, 'customer': customer,
               'customer_end': customer_end, 'goods': goods, 'goods_end': goods_end}
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
            model_field = dict_model._meta.get_field(field)
            if model_field.get_internal_type() == 'ForeignKey':
                setattr(dict_element, field, model_field.related_model.objects.get(id=request.POST[field]))
            elif model_field.get_internal_type() == 'Boolean':
                setattr(dict_element, field, False)
                if request.POST[field]:
                    setattr(dict_element, field, True)
            else:
                setattr(dict_element, field, request.POST[field])
    dict_element.save()
    return HttpResponse()


def dictionary_json(request, dict_type, id_no, order):
    dict_model = getattr(models, dict_type)
    if order == 'default':
        order = dict_model.order_default()
    dict_items = dict_model.objects.all().order_by(*order)[id_no + 1: id_no + 21]
    json_dict = serialize('python', dict_items)
    json_dict = json.dumps(json_dict, ensure_ascii=False, default=str)
    return JsonResponse(json_dict, safe=False)


def customer_group_json(request):
    customer_groups = CustomerGroups.objects.all().order_by('group_name')
    json_dict = serialize('python', customer_groups)
    json_dict = json.dumps(json_dict, ensure_ascii=False, default=str)
    return JsonResponse(json_dict, safe=False)
