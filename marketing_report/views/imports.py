from django.shortcuts import render


def imports(request):
    navi = 'imports'
    context = {'navi': navi}
    return render(request, 'import.html', context)