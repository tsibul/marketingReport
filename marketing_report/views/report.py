from django.shortcuts import render
from marketing_report.models.report_period import *
from marketing_report.models.report_classes import *
from marketing_report.models.argument_classes import *


def reports(request):
    periods = ReportPeriod.calculable_list()
    cst_reports = cst_report_list()
    goods_reports = goods_report_list()
    json_cst_reports = json_customer_report_list()
    json_goods_reports = json_goods_report_list()
    money_arguments = money_argument_list()
    json_money_arguments = json_money_argument_list()
    json_time_arguments = json_time_argument_list()

    context = {'periods': periods, 'cst_reports': cst_reports, 'goods_reports': goods_reports,
               'json_goods_reports': json_goods_reports, 'json_cst_reports': json_cst_reports,
               'money_arguments': money_arguments, 'json_money_arguments': json_money_arguments,
               'json_time_arguments': json_time_arguments}
    return render(request, 'report.html', context)
