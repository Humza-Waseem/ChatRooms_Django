from django.shortcuts import render
from django.http import HttpResponse
from .models import Room




# rooms = [
#     {'id': 1, 'name': 'Lets learn Python'},
#     {'id': 2, 'name': 'Designing a Django App'},
#     {'id': 3, 'name': 'Frontend Development'},
# ]
def home(request):
    # context = {
    #     "homepage":"THis is the HOME page variable "
    # }
    # return render(request, 'home.html',context)   The context variable is used to pass the data from the views.py to the html page, we can pass the data in the form of dictionary, list, tuple, etc.

    #!####### using render function to render the home.html page, we could have used HttpResponse() function to render the page, but it is not a good practice to use it, so we use render() function and render it to a html page
    rooms = Room.objects.all()
    context = { 'rooms': rooms}

    return render(request, 'base/home.html', context    )   #  we passed the rooms named dictionary to the home.html page ..  The first 'rooms' is the variable name that we will use in the html page and the second 'rooms' is the dictionary name that we created above(the dictionary that we are passing on by render function to the home.html page)


def room(request,pk): 
    room = Room.objects.get(id = pk)
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    context = { 'room': room}
    

    return render(request, 'base/room.html',context)   ## using render function to render the room.html page
  
def test(request):
    return render(request, 'base/test.html')   ## using render function to render the test.html page

