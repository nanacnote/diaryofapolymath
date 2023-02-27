from django.shortcuts import render


def index(request):
    payload = dict()
    return render(request, "exclusive/index.html", payload)
