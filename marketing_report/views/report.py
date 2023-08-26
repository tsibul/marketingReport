from django.http import JsonResponse
from django.shortcuts import render
from marketing_report.models.report_period import *
from marketing_report.models.report_classes import *
from marketing_report.models.argument_classes import *


def reports(request):
    navi = 'reports'
    periods = ReportPeriod.calculable_list()
    cst_reports = cst_report_list()
    goods_reports = goods_report_list()
    json_cst_reports = json_customer_report_list()
    json_goods_reports = json_goods_report_list()
    money_arguments = money_argument_list()
    json_money_arguments = json_money_argument_list()
    json_time_arguments = json_time_argument_list()
    json_period = json_periods()

    context = {'periods': periods, 'cst_reports': cst_reports, 'goods_reports': goods_reports,
               'json_goods_reports': json_goods_reports, 'json_cst_reports': json_cst_reports,
               'money_arguments': money_arguments, 'json_money_arguments': json_money_arguments,
               'json_time_arguments': json_time_arguments, 'json_period': json_period, 'navi': navi}
    return render(request, 'report.html', context)


def json_report(request, report_no, report_type, period, date_begin, date_end, argument):
    return JsonResponse('', safe=False)