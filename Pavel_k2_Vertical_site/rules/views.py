from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def rules(request):
    template = "rules/index.html"
    return render(request, template)