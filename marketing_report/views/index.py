from datetime import datetime

from django.shortcuts import render

from marketing_report.models import ReportPeriod, json_periods
from marketing_report.models.argument_classes import money_argument_list, time_argument_list, json_money_argument_list, \
    json_time_argument_list
from marketing_report.models.report_classes import cst_report_list, goods_report_list, money_report_list


def index(request):
    navi = 'main'
    periods = ReportPeriod.calculable_list()
    cst_reports = cst_report_list()
    goods_reports = goods_report_list()
    money_arguments = money_argument_list()
    time_arguments = time_argument_list()
    json_money_arguments = json_money_argument_list()
    json_time_arguments = json_time_argument_list()
    json_period = json_periods()
    money_reports = money_report_list()
    year = datetime.now().year - 1

    context = {'periods': periods, 'cst_reports': cst_reports, 'goods_reports': goods_reports,
               'money_arguments': money_arguments, 'json_money_arguments': json_money_arguments,
               'json_time_arguments': json_time_arguments, 'json_period': json_period, 'time_arguments': time_arguments,
               'money_reports': money_reports, 'navi': navi, 'year': year}
    return render(request, 'index.html', context)