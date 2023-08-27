from django.shortcuts import render


def dictionary(request):
    navi = 'dictionary'
    context = {'navi': navi}
    return render(request, 'dictionary.html', context)