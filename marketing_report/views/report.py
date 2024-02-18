import datetime

from django.http import JsonResponse
from django.shortcuts import render
from marketing_report.models.report_period import ReportPeriod, json_periods, find_all_period_by_date_range
from marketing_report.models.report_classes import cst_report_list, goods_report_list, json_goods_report_list, \
    json_customer_report_list, money_report_list
from marketing_report.models.argument_classes import json_time_argument_list, json_money_argument_list, \
    money_argument_list, time_argument_list


def reports(request):
    navi = 'reports'
    periods = ReportPeriod.calculable_list()
    cst_reports = cst_report_list()
    goods_reports = goods_report_list()
    json_cst_reports = json_customer_report_list()
    json_goods_reports = json_goods_report_list()
    money_arguments = money_argument_list()
    time_arguments = time_argument_list()
    json_money_arguments = json_money_argument_list()
    json_time_arguments = json_time_argument_list()
    json_period = json_periods()
    money_reports = money_report_list()

    context = {'periods': periods, 'cst_reports': cst_reports, 'goods_reports': goods_reports,
               'json_goods_reports': json_goods_reports, 'json_cst_reports': json_cst_reports,
               'money_arguments': money_arguments, 'json_money_arguments': json_money_arguments,
               'json_time_arguments': json_time_arguments, 'json_period': json_period, 'time_arguments': time_arguments,
               'money_reports': money_reports, 'navi': navi}
    return render(request, 'report.html', context)


def json_report(request, report_class, report_type, period, parameter, begin, end):
    date_begin = datetime.date(int(begin), 1, 1)
    date_end = datetime.date(int(end), 12, 31)
    period_name = 'помесячно' if period == 'MT' else ('поквартально' if period == 'QT' else 'по годам')
    period_query = find_all_period_by_date_range(date_begin, date_end).filter(period=period).order_by('date_begin')
    try:
        num = int(parameter)
        parameter_name = (next(filter(lambda param: param.code == parameter, time_argument_list()), None)).description
    except:
        parameter_name = (next(filter(lambda param: param.code == parameter, money_argument_list()), None)).description
    if report_class == 'customer':
        report_obj = (next(filter(lambda report: report.code == report_type, cst_report_list()), None))
        report_result = report_obj.report_function(period_query, parameter)
        report_name = 'Клиенты ' + report_obj.description
    elif report_class == 'goods':
        report_obj = (next(filter(lambda report: report.code == report_type, goods_report_list()), None))
        report_result = report_obj.report_function(period_query, parameter)
        report_name = 'Товары ' + report_obj.description
    else:
        report_result = None
        report_name = None
    final_report = {'report_name': report_name, 'period': period_name, 'parameter': parameter_name,
                    'date_begin': date_begin, 'date_end': date_end, 'period_data': list(period_query.values('name')),
                    'report_data': report_result}
    return JsonResponse(final_report, safe=False)
