from django.shortcuts import render
from django.http import HttpResponse



def home(request):
    context = {
        "homepage":"THis is the HOME page variable "
    }
    return render(request, 'home.html',context)   ## using render function to render the home.html page, we could have used HttpResponse() function to render the page, but it is not a good practice to use it, so we use render() function and render it to a html page
def room(request): 
    context = {
        "rooms":"THis is the room page variable "
    }
    return render(request, 'room.html',context)   ## using render function to render the room.html page
  

