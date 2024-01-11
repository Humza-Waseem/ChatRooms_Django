from django.shortcuts import render
from django.http import HttpResponse



def home(request):
    return HttpResponse("Home page From base/views.py")

def room(request):
    return HttpResponse("Room page From base/views.py")


