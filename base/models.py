from django.db import models
from django.contrib.auth.models import User



# Create your models here.

##  This is the model for the topic that we will be creating
class Topic(models.Model):
    name = models.TextField(max_length=100)    
   
    def __str__(self):
        return self.name

# This is the model for the room that we will be creating
class Room(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null = True, blank = True)   #  setting to null means that it will be blank in the database if not filled out at runtime otherwise the data basebase will consider it as missing data   # blank means that it is not required to be filled out at runtime 
    # participants =

    host = models.ForeignKey(User, on_delete =  models.SET_NULL, null = True)   # when the user is deleted then all its rooms are delete as well
    topic = models.ForeignKey(Topic, on_delete =  models.SET_NULL, null = True)   # when the topic is deleted then all the rooms of that topic will be deleted as well
    updated = models.DateTimeField(auto_now=True)  # auto_now will update the time whenever the room is updated
    created = models.DateTimeField(auto_now_add=True)  # auto_now_add will update the time only when the room is created for the first time

    def __str__(self):
        return self.name
    
    
    #DECLARING THE CLASS HERE THAT WILL BE USEFULL TO IMPLEMENT SOME OPERATIONS ON THE SPECIFIC MODULE
    class Meta:
        ordering = ['-updated','-created']   # here we are ordering the rooms according to the most recent updated and created room in the list..     The ( - ) sign means to update according to most recent....


##  This is the model for the message that we will be creating
class Message(models.Model):
    user = models.ForeignKey(User, on_delete =  models.CASCADE)   # when the user is deleted then all its messages are delete as well
                # WHEN       USER IS DELETED THEN DELETE ALL MESSAGES
    body = models.CharField(max_length=1000)  # the body of the message
    room = models.ForeignKey(Room, on_delete =  models.CASCADE) 
                # WHEN       ROOM IS DELETED THEN DELETE ALL MESSAGES 
    # THE RELATION OF ROOM TO MESSAGES WILL BE (ONE TO MANY)this is the foreign key that we will be using to connect the message with the room, on_delete=models.CASCADE means that if the room is deleted then the message will also be deleted
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50] # this will return the first 50 characters of the message body


