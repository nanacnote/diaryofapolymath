from django.shortcuts import render


def index(request):
    payload = dict()
    return render(request, "projects/index.html", payload)


def post(request, slug):
    payload = dict()
    return render(request, "projects/post.html", payload)
