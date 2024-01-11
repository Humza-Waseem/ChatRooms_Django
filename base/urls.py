from django.urls import path
from . import views  # we have imported views from base/views.py  that is in the same directory, so we used "." to import from the same directory


############  here we have made a list of url paterns    ###############
urlpatterns  = [
    path('', views.home, name='home'), # the path() function takes 3 arguments: 1st is the url, 2nd is the view function, 3rd is the name of the url

    path('room/',  views.room, name ="room")     #  the name is optional, but it is good to use it
    
]
