from django.shortcuts import render


def index(request):
    payload = dict()
    return render(request, "blog/index.html", payload)


def post(request, slug):
    payload = dict()
    return render(request, "blog/post.html", payload)
