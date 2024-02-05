import json
from datetime import timedelta, date, datetime

from django.core.serializers import serialize
from django.db.models import Max
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from marketing_report import models
from marketing_report.models import CustomerGroup, Color

from marketing_report.service_functions import linking_filter


def dictionary(request):
    border_date = date.today() - timedelta(days=1100)
    navi = 'dictionary'
    context = {'navi': navi, 'border_date': border_date}
    return render(request, 'dictionary.html', context)


@csrf_exempt
def dictionary_update(request, dict_type):
    dict_id = request.POST['id']
    dict_model = getattr(models, dict_type)
    field_list = [f.name for f in dict_model._meta.get_fields()]
    if dict_id != '0':
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


def dictionary_json(request, dict_type, id_no, order, search_string):
    dict_items = dict_additional_filter(dict_type, order, id_no, search_string)
    formatted_dict_items = [format_datetime_fields(item) for item in dict_items]
    return JsonResponse(formatted_dict_items, safe=False)


def dictionary_json_filter(request, dict_type, filter_dictionary, filter_dictionary_id):
    """
    Using for table connection if we find item in second table in second table
    filter parent table by it
    :param request:
    :param dict_type:
    :param filter_dictionary:
    :param filter_dictionary_id:
    :return:
    """
    if dict_type == 'default':
        formatted_dict_items = []
        json_dict = json.dumps(formatted_dict_items, ensure_ascii=False, default=str)
        return JsonResponse(json_dict, safe=False)
    dict_model = getattr(models, dict_type)
    if filter_dictionary != 'default':
        filter_model = getattr(models, filter_dictionary)
        filter_item = linking_filter(dict_model, filter_model, filter_dictionary_id)
    else:
        filter_item = dict_model.objects.all()
    formatted_dict_items = [{item.id: str(item)} for item in filter_item]
    json_dict = json.dumps(formatted_dict_items, ensure_ascii=False, default=str)
    return JsonResponse(json_dict, safe=False)


def dict_additional_filter(dict_type, order, id_no, search_string):  # костыль
    border_date = date.today() - timedelta(days=1100)
    dict_model = getattr(models, dict_type)
    if order == 'default':
        order = dict_model.order_default()
    if search_string == 'default':
        if dict_type == 'Customer':
            dict_items = dict_model.objects.filter(internal=False, date_last__gt=border_date).order_by(*order)
            # dict_items = dict_model.objects.filter(internal=False).order_by(*order)
        elif dict_type == 'CustomerGroups':
            dict_items = dict_model.objects.filter(date_last__gt=border_date, deleted=False).order_by(*order)
            # dict_items = dict_model.objects.filter(deleted=False).order_by(*order)
        else:
            dict_items = dict_model.objects.filter(deleted=False).order_by(*order)
    elif search_string == '%inactive%':
        if dict_type == 'Customer':
            # dict_items = dict_model.objects.filter(internal=False, date_last__gt=border_date).order_by(*order)
            dict_items = dict_model.objects.filter(internal=False).order_by(*order)
        elif dict_type == 'CustomerGroups':
            # dict_items = dict_model.objects.filter(date_last__gt=border_date, deleted=False).order_by(*order)
            dict_items = dict_model.objects.filter(deleted=False).order_by(*order)
    else:
        search_string = search_string.replace('_', ' ')
        if dict_type == 'Customer':
            # filter_items = dict_model.objects.filter(internal=False, date_last__gt=border_date).order_by(*order)
            filter_items = dict_model.objects.filter(internal=False).order_by(*order)
        elif dict_type == 'CustomerGroups':
            # filter_items = dict_model.objects.filter(date_last__gt=border_date, deleted=False).order_by(*order)
            filter_items = dict_model.objects.filter(date_last__gt=border_date).order_by(*order)
        else:
            filter_items = dict_model.objects.filter(deleted=False).order_by(*order)
        dict_items = filter_items.filter(id=0)
        for field in dict_model._meta.get_fields():
            if field.get_internal_type() == 'CharField':
                field_name = field.name + '__icontains'
                dict_items = dict_items | filter_items.filter(**{field_name: search_string})
            elif field.get_internal_type() == 'ForeignKey':
                foreign_model = field.related_model
                for key in foreign_model._meta.get_fields():
                    if key.get_internal_type() == 'CharField':
                        field_name = field.name + '__' + key.name + '__icontains'
                        dict_items = dict_items | filter_items.filter(**{field_name: search_string})
    dict_items = dict_items.distinct()[id_no: id_no + 20]
    return dict_items


def customer_group_json(request):
    customer_groups = CustomerGroup.objects.filter(deleted=False).order_by('group_name')
    json_dict = serialize('python', customer_groups)
    json_dict = json.dumps(json_dict, ensure_ascii=False, default=str)
    return JsonResponse(json_dict, safe=False)


def dictionary_delete(request, dict_type, id_no):
    dict_model = getattr(models, dict_type)
    dict_element = dict_model.objects.get(id=id_no)
    dict_element.deleted = True
    dict_element.save()
    return HttpResponse()


def dictionary_last_id(request, dict_type):
    dict_model = getattr(models, dict_type)
    last_id = dict_model.objects.filter(deleted=False).aggregate(Max('id'))
    json_dict = json.dumps(last_id, ensure_ascii=False, default=str)
    return JsonResponse(json_dict, safe=False)


def format_datetime_fields(item):
    """
    Format date field and return hex color if exists
    :param item:
    :return:
    change datetime param fo js, returns hex color if exists
    """
    formatted_item = {}
    item_dict = item.__dict__
    try:
        formatted_item['hex'] = Color.objects.get(id=item.color.id).color_code
    except:
        pass
    for field in item_dict.keys():
        if isinstance(item_dict[field], datetime):
            formatted_item[field] = item_dict[field].strftime('%d.%m.%y %H:%M')
        else:
            if field[0:1] != "_":
                formatted_item[field] = item_dict[field]
                if field[-3:] == "_id":
                    if type(getattr(item, field[0:-3])).__name__ == 'User':
                        formatted_item[field[0:-3]] = getattr(getattr(item, field[0:-3]), 'last_name')
                    else:
                        formatted_item[field[0:-3]] = str(getattr(item, field[0:-3]))
    return formatted_item
