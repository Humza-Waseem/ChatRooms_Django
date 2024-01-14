from django.db import models

# Create your models here. 
#here we will create our database models 

class Room(models.Model):
    #host = 
    #topic =
    name = models.CharField(max_length=50)
    description = models.TextField(null = True, blank = True) # here we are making the description field optional so a person can make a room and the description can be black , ( blank = True),,,,,,,,,,, (null = True) means that the description field in the data base can be empty.
    #participants =

    created = models.DateTimeField(auto_now_add=True) # this will automatically add the time when the room is created
    updated = models.DateTimeField(auto_now=True) # this will automatically update the time when the room is updated

    def __str__(self):
        return self.name
    

