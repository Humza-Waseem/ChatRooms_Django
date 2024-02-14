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
    path('', include ("base.urls") ),
    path('api/', include ("base.api.urls") ),# any url that starts with 'api/' will be redirected to the urls.py file in the base/api directory
    
    
]
