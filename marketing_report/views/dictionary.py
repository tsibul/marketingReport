from django.shortcuts import render
from marketing_report.models.color_models import PrintType, ColorScheme
from marketing_report.models.goods_types_models import GoodCrmType, GoodMatrixType


def dictionary(request):
    navi = 'dictionary'
    matrix = GoodMatrixType.objects.all().order_by('matrix_name')
    crm = GoodCrmType.objects.all().order_by('crm_name')
    print_type = PrintType.objects.all().order_by('type_name')
    color_group = ColorScheme.objects.all().order_by('scheme_name')
    context = {'navi': navi, 'matrix': matrix, 'crm': crm, 'print_type': print_type, 'color_group': color_group}
    return render(request, 'dictionary.html', context)