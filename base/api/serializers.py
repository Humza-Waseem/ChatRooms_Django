# In this file we will create a serializer for the our python models. A serializer is a class that converts complex data types, such as querysets and model instances, into native Python datatypes that can be rendered into JSON.

from rest_framework.serializers import ModelSerializer
from base.models import Room

class RoomSerializer(ModelSerializer): # taking the ROOM Model And converting it into a JSON object(serializing it)
    class Meta:
        model = Room
        fields = '__all__'

