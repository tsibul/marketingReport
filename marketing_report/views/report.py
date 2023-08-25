from django.shortcuts import render
from marketing_report.models.report_period import *


def reports(request):
    periods = ReportPeriod.calculable_list()
    context = {'periods': periods}
    return render(request, 'report.html', context)
