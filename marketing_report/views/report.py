import json
from django.core.serializers import serialize
from django.shortcuts import render
from marketing_report.models.report_period import *
from marketing_report.models.report_types import *


def reports(request):
    periods = ReportPeriod.calculable_list()
    cst_reports = cst_report_list()
    goods_reports = goods_report_list()
    json_cst_reports = json_customer_report_list()
    json_goods_reports = json_goods_report_list()

    context = {'periods': periods, 'cst_reports': cst_reports, 'goods_reports': goods_reports,
               'json_goods_reports': json_goods_reports, 'json_cst_reports': json_cst_reports}
    return render(request, 'report.html', context)
