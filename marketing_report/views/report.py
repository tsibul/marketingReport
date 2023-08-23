from django.shortcuts import render


def reports (request):
    context = {}
    return render(request, 'report.html', context)

