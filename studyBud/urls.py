from django.contrib import admin
from django.urls import path 
from django.urls import include

# from django.http import HttpResponse

# def home(request):
#     return HttpResponse("Home page")

# def room(request):
#     return HttpResponse("Room page")

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('room/', room),
    path('', include ("base.urls") )
    # path("", home),
    # path('', include('base.urls'))
    
]
