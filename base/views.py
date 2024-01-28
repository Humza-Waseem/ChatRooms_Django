from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic   # importing the Room and Topic models from models which is in the same directory
from django.contrib import messages  # importing the flash messages 
from .Forms import RoomForm  
from django.contrib.auth import authenticate,login,logout  
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # here we get Q because it will help us to insert query operations AND,OR,NOT



def UserLogout(request):  # creating this view to so that   
    logout(request)   # user presses the logout button then its session will be deleted from the database
    return redirect('home')   # and the user is redirected to the home page..

def registerUser(request):
    # page = 'register' 
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
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
        username = request.POST.get('username').lower() # getting the username from the login form in lowercase
        password = request.POST.get('password')  # getting the password from the login form
        
        try:
            user = User.objects.get(username=username) # getting the user with the specific username
        except:
            messages.error(request,"UserName does not exist")
        
        user = authenticate(request,username =username,password= password )
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Username or Password is incorrect")

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
        Q(topic__name__icontains=q) | # filter if the q is in the topic name(q will be entered by user through SearchBar)
        Q(name__icontains =q)   |      # OR   q entered by user through SEarchBar is included in the name of room
        Q(description__icontains =q))    

    topics = Topic.objects.all()
    context = { 'rooms': rooms,'topics':topics}

    return render(request, 'base/home.html', context    )   #  we passed the rooms named dictionary to the home.html page ..  The first 'rooms' is the variable name that we will use in the html page and the second 'rooms' is the dictionary name that we created above(the dictionary that we are passing on by render function to the home.html page)


def room(request,pk):     
    room = Room.objects.get(id = pk)
    UserMessages = room.message_set.all().order_by('-created')  # getting all the messages of the room and ordering them according to the most recent message

    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    context = { 'room': room,'messages':UserMessages}
    

    return render(request, 'base/room.html',context)   ## using render function to render the room.html page
  

@login_required(login_url="UserLogin")     # login will be required to access this page
def CreateRoom(request):
    form = RoomForm()   # This line creates an instance of the RoomForm class.
    if request.method =='POST':   # This line checks if the HTTP request method is 'POST'
        form = RoomForm(request.POST)  #  passing all the values into the form ,, adding the date to form
        if form.is_valid():   # this check if all the form submitted values are valid
            form.save()   ## saving the form
            return redirect('home')    # here we redirect the user (who submit the form) to the listed Page(home) note that we are using the Name of the 'HOME' html file which we declared in the urls. 

    context = {'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url="UserLogin")
def UpdateRoom(request,pk):  # here we get the pk also to update the specific room
    room = Room.objects.get(id = pk)  # getting the room with the specific id
    form = RoomForm(instance= room)  # here we get the instance of the room that we want to update. THis will also show  the data of the room that we want to update in the form fields... so it would be easy for update keeping in view the previous data
    if request.user != room.host:
        return HttpResponse("You are not allowed to Edit this page")
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance= room)  # Updating the form according to the the room.  The instance=room tells the request to update the attributes.. if we do not do this then django will simply make another room with our updated values
        if form.is_valid():
            form.save()
            return redirect('home')  # going back to the home page 
    context = {'form':form}

    return render(request,'base/room_form.html',context)


@login_required(login_url="UserLogin")
def DeleteRoom(request,pk):
    room = Room.objects.get(id = pk)   # getting the specific room 
    if request.method == 'POST': # if the method is to POST (form is filled)then
        room.delete()    # delete the room 
        return redirect('home')   # redirect the user to home. after deleting the room 
    context = {'obj':room}  # using obj instead of "room" because we will use obj in our template to show a delete message also if the message isn't about the room 
    
    return render(request,'base/delete.html',context)