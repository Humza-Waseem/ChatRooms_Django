from django.forms import ModelForm
from .models import Room

# for creating forms we use this......


## this is a RoomForm where we will be creating the form for the room model(containing the fields of the room model)
class RoomForm (ModelForm):
    class Meta:
        model = Room  
        # model = Room
        fields = '__all__'  # this will create a form with all the fields of the Room model,,,we can also take specific fields from the model and create a form with those fields only
        exclude =[ 'host', 'participants']