from django.shortcuts import render


def page_not_found(request, exception):
    template = 'pages/404.html'
    return render(request, template, status=404)


def csrf_failure(request, reason=''):
    template = 'pages/403.html'
    return render(request, template, status=403)


def internal_error(request):
    template = 'pages/500.html'
    return render(request, template, status=500)
