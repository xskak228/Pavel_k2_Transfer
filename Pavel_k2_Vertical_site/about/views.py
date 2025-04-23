from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def about(request):
    template = "about/index.html"
    return render(request, template)