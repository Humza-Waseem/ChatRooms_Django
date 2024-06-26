from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic,Message,User   # importing the Room and Topic and Message models from models which is in the same directory
from django.contrib import messages  # importing the flash messages 

from .Forms import RoomForm , UserForm, MyUserCreationForm  # importing the RoomForm  and UserFOrm from the Forms.py file which is in the same directory
from django.contrib.auth import authenticate,login,logout  
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # here we get Q because it will help us to insert query operations AND,OR,NOT




def UserLogout(request):  # creating this view to so that   
    logout(request)   # user presses the logout button then its session will be deleted from the database
    return redirect('home')   # and the user is redirected to the home page..

def registerUser(request):  
    # page = 'register' 
    # form = UserCreationForm()
    form = MyUserCreationForm()
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = MyUserCreationForm(request.POST)   # using MyUserCreationForm because it has our custom user model form
        if form.is_valid():
            user = form.save(commit=False)#commit = False means that we are not saving the form yet
            user.username = user.username
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')

    return render(request,'base/UserLogin.html',{'form':form})


def UserLogin(request):
    page  = 'login'
    if request.user.is_authenticated: # if a authenticated user try to manually enter "/login" in the browser then we will restrict the Login page
        return redirect('home') # and rediredct the user to the home page because uer is already logged in
    
    if request.method == "POST":  
        email = request.POST.get('email') # getting the email from the login form in lowercase
        password = request.POST.get('password')  # getting the password from the login form
        
        try:
            user = User.objects.get(email=email) # getting the user with the specific username
        except:
            messages.error(request,"email does not exist")
        
        user = authenticate(request,email =email,password= password )
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"email or Password is incorrect")

    context={'page':page}
    return render(request,'base/UserLogin.html',context)

# rooms = [
#     {'id': 1, 'name': 'Lets learn Python'},
#     {'id': 2, 'name': 'Designing a Django App'},
#     {'id': 3, 'name': 'Frontend Development'},
# ]



def home(request):
    
    q = request.GET.get('q') if( request.GET.get('q') != None) else ''  # getting the query from the search bar and if it is not there then set it to empty string

   
    # rooms = Room.objects.filter(topic__name__icontains=q) # this will only allow us to search for the topic name

    rooms = Room.objects.filter(    
        Q(topic__name__icontains=q) | # filter if the q is in the topic name OR Name of room OR in the Description(q will be entered by user through SearchBar)
        Q(name__icontains =q)  |
        Q(description__icontains =q))   
     # if we do not give anything in the search bar then it will show all the rooms and the  filter will not be applied

    topics = Topic.objects.all()
    UserMessages = Message.objects.filter(  Q(room__topic__name__icontains = q))  # filtering the messages according to the topic name
    room_count = rooms.count()  # getting the count of the rooms
    context = { 'rooms': rooms,'topics':topics,'UserMessages':UserMessages,"room_count": room_count}

    return render(request, 'base/home.html', context    )   #  we passed the rooms named dictionary to the home.html page ..  The first 'rooms' is the variable name that we will use in the html page and the second 'rooms' is the dictionary name that we created above(the dictionary that we are passing on by render function to the home.html page)

@login_required(login_url="UserLogin") 
def UserProfile(request,pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()  # getting all the rooms of the user
    topics = Topic.objects.all()
    UserMessages = user.message_set.all()

    context = {"user": user,"rooms":rooms , "topics":topics , "UserMessages":UserMessages}
    return render(request,'base/userProfile.html',context)


@login_required(login_url="UserLogin") 
def UpdateUser(request):
    form = UserForm(instance = request.user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance= request.user)
        if form.is_valid():
            form.save()
            return redirect('UserProfile',pk = request.user.id)

    context= {"form":form}
    return render(request,'base/UpdateUser.html',context)


def room(request,pk):     
    room = Room.objects.get(id = pk) 
    UserMessages = room.message_set.all()  # getting all the messages of the room and ordering them according to the most recent message  ( It is a "1 to many relationship" so we can use the message_set to get all the messages of the room)
    participants = room.participants.all()  # getting all the participants of the room

    # Form for sending the message in the room.html page
    if(request.method == 'POST'):     # if the method in the form is POST then
        message = Message.objects.create(    # creating the message object
        user= request.user,                  # the user will be the user who is logged in
        room = room,                         # the room will be the room in which the message is sent
        body = request.POST.get('body') # the actual message is one which is entered by the user in the field which is named as 'body' in the FormField of the room.html page
        )
        room.participants.add(request.user)  # adding the user who has sent the message to the participants of room

        return redirect('room',pk=room.id)   # redirecting the user to the same room after sending the message.. This will refresh the page and the message will be shown in the room.html page
    

    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    context = { 'room': room,'UserMessages':UserMessages,'participants':participants}
    

    return render(request, 'base/room.html',context)   ## using render function to render the room.html page
  

@login_required(login_url="UserLogin")     # login will be required to access this page
def CreateRoom(request):
    form = RoomForm()   # This line creates an instance of the RoomForm class.
    topics = Topic.objects.all( )          # Getting all the topics from the database

    if request.method =='POST':   # This line checks if the HTTP request method is 'POST'
        topic_name = request.POST.get('topic')  # getting the topic name from the form
        topic, created = Topic.objects.get_or_create(name=topic_name)  # getting the topic from the database if it is already there otherwise create the topic
        Room.objects.create(  # creating the room object
            host = request.user,  # the host will be the user who is logged in
            topic = topic,        # the topic will be the topic that we got from the form
            name = request.POST.get('name'),  # getting the name of the room from the form
            description = request.POST.get('description'),  # getting the description of the room from the form
        )
        # form = RoomForm(request.POST)  #  passing all the values into the form ,, adding the date to form
        # if form.is_valid():   # this check if all the form submitted values are valid

        #     room = form.save(commit= False)  # here we save the form, getting the instance of the form 
        #     room.host = request.user
            
            # room.save()
              
        return redirect('home')    # here we redirect the user (who submit the form) to the listed Page(home) note that we are using the Name of the 'HOME' html file which we declared in the urls. 

    context = {'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url="UserLogin")
def UpdateRoom(request,pk):  # here we get the pk also to update the specific room
    room = Room.objects.get(id = pk)  # getting the room with the specific id
    form = RoomForm(instance= room)  # here we get the instance of the room that we want to update. THis will also show  the data of the room that we want to update in the form fields... so it would be easy for update keeping in view the previous data
    topics = Topic.objects.all()  # getting all the topics from the database
    if request.user != room.host:
        return HttpResponse("You are not allowed to Edit this page")
    
    # if request.method == 'POST':
    #     form = RoomForm(request.POST, instance= room)  # Updating the form according to the the room.  The instance=room tells the request to update the attributes.. if we do not do this then django will simply make another room with our updated values

    if request.method == 'POST':
        topic__name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic__name)
        room.name= request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        # if form.is_valid():
        #     form.save()
        return redirect('home')  # going back to the home page 
    context = {'form':form,'topics': topics,'room':room}

    return render(request,'base/room_form.html',context)


@login_required(login_url="UserLogin")
def DeleteRoom(request,pk):
    room = Room.objects.get(id = pk)   # getting the specific room 
    if request.method == 'POST': # if the method is to POST (form is filled)then
        room.delete()    # delete the room 
        return redirect('home')   # redirect the user to home. after deleting the room 
    context = {'obj':room}  # using obj instead of "room" because we will use obj in our template to show a delete message also if the message isn't about the room 
    
    return render(request,'base/delete.html',context)

@login_required(login_url="UserLogin")
def DeleteMessage(request,pk):
    messages = Message.objects.get(id = pk)   

    if( request.user != messages.user ): 
        return HttpResponse("You are not allowed to delete this message")

    if request.method == 'POST': 
        messages.delete()
        return redirect('room',pk=messages.room.id)   # redirecting the user to the same room after deleting the message
    
    context = {'obj':messages} 
    
    return render(request,'base/delete.html',context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})