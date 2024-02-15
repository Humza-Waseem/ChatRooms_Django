from django.contrib import admin

# Register your models here.
from .models import Room,Topic,Message,User # here we import the Room class from models.py

admin.site.register(Room)  # here we have registered the Room class with the admin site so we can see it in the admin page
admin.site.register(Topic)
admin.site.register(Message)

admin.site.register(User)# the custom user model we created in the models.py file