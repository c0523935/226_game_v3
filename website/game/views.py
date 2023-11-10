from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello world Alan')


def index2(request):
    return HttpResponse('create player')
# Create your views here.
