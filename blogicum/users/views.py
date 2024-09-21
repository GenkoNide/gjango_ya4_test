from django.shortcuts import render


def login(request):
    template = 'registration/login.html'
    return render(request, template)
