from django.shortcuts import render


def index(request):
    navi = 'main'
    context = {'navi': navi}
    return render(request, 'index.html', context)