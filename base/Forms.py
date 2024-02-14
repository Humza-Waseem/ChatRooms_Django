from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User   #importing the user model from the django built in models

class UserForm(ModelForm):  #creating a class that inherits properties from the ModelForm class,,,, We will use it in the UpdateUser View.. To make a form that will include all the fields of the user model.
    class Meta:
        model = User
        fields = ['username','email']



## this is a RoomForm where we will be creating the form for the room model(containing the fields of the room model)
class RoomForm (ModelForm):
    class Meta:
        model = Room  
        # model = Room
        fields = '__all__'  # this will create a form with all the fields of the Room model,,,we can also take specific fields from the model and create a form with those fields only
        exclude =[ 'host', 'participants']