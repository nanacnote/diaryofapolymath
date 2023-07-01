from django.shortcuts import render


def index(request):
    context = dict()
    return render(request, "exclusive/index.html", context)
