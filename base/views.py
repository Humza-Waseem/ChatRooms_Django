from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic
from .Forms import RoomForm
from django.db.models import Q  # here we get Q because it will help us to insert query operations AND,OR,NOT





# rooms = [
#     {'id': 1, 'name': 'Lets learn Python'},
#     {'id': 2, 'name': 'Designing a Django App'},
#     {'id': 3, 'name': 'Frontend Development'},
# ]
def home(request):
    
    q = request.GET.get('q') if( request.GET.get('q') != None) else ''  # getting the query from the search bar and if it is not there then set it to empty string

   
    # rooms = Room.objects.filter(topic__name__icontains=q) # this will only allow us to search for the topic name
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | # filter if the q is in the topic name(q will be entered by user through SearchBar)
        Q(name__icontains =q)   |      # OR   q entered by user through SEarchBar is included in the name of room
        Q(description__icontains =q))    

    topics = Topic.objects.all()
    #!####### using render function to render the home.html page, we could have used HttpResponse() function to render the page, but it is not a good practice to use it, so we use render() function and render it to a html page
    context = { 'rooms': rooms,'topics':topics}

    return render(request, 'base/home.html', context    )   #  we passed the rooms named dictionary to the home.html page ..  The first 'rooms' is the variable name that we will use in the html page and the second 'rooms' is the dictionary name that we created above(the dictionary that we are passing on by render function to the home.html page)


def room(request,pk):     
    room = Room.objects.get(id = pk)
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    context = { 'room': room}
    

    return render(request, 'base/room.html',context)   ## using render function to render the room.html page
  

def CreateRoom(request):
    form = RoomForm()   # This line creates an instance of the RoomForm class.
    if request.method =='POST':   # This line checks if the HTTP request method is 'POST'
        form = RoomForm(request.POST)  #  passing all the values into the form ,, adding the date to form
        if form.is_valid():   # this check if all the form submitted values are valid
            form.save()   ## saving the4 form
            return redirect('home')    # here we redirect the user (who submit the form) to the listed Page(home) note that we are using the Name of the 'HOME' html file which we declared in the urls. 

    context = {'form':form}
    return render(request,'base/room_form.html',context)


def UpdateRoom(request,pk):  # here we get the pk also to update the specific room
    room = Room.objects.get(id = pk)  # getting the room with the specific id
    form = RoomForm(instance= room)  # here we get the instance of the room that we want to update. THis will also show  the data of the room that we want to update in the form fields... so it would be easy for update keeping in view the previous data

    if request.method == 'POST':
        form = RoomForm(request.POST, instance= room)  # Updating the form according to the the room.  The instance=room tells the request to update the attributes.. if we do not do this then django will simply make another room with our updated values
        if form.is_valid():
            form.save()
            return redirect('home')  # going back to the home page 
    context = {'form':form}

    return render(request,'base/room_form.html',context)

def DeleteRoom(request,pk):
    room = Room.objects.get(id = pk)   # getting the specific room 
    if request.method == 'POST': # if the method is to POST (form is filled)then
        room.delete()    # delete the room 
        return redirect('home')   # redirect the user to home. after deleting the room 
    context = {'obj':room}  # using obj instead of "room" because we will use obj in our template to show a delete message also if the message isn't about the room 
    return render(request,'base/delete.html',context)