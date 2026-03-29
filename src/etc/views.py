from django.shortcuts import render


def index(request):
    context = dict()
    return render(request, "etc/index.html", locals())
