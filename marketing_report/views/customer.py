from django.shortcuts import render


def customer(request):
    navi = 'customer'
    context = {'navi': navi}
    return render(request, 'customer.html', context)
