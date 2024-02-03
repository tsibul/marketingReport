from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/marketing')
        else:
            pass
    return redirect('/marketing')


def custom_logout(request):
    logout(request)
    return redirect('/marketing')

