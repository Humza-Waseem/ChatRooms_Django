from django.http import JsonResponse  # importing the JsonResponse which will be used to return the response in the form of json.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer


@api_view(['GET'])  # here we are using the api_view decorator to specify the type of request that the view function can handle. In this case, it can handle the GET request.
def getRoutes(request):
    routes =[
        'GET /api/', 
        'GET /api/rooms',  
        'GET /api/rooms/:id' 
    ]
    return Response(routes)

    #return JsonResponse(routes, safe=False)  # here we are returning the response in the form of json, The JSON response will convert the data in the view into JSON data. Safe = False allow us to use data other than the python dictionaries in our response. 

@api_view(['GET'])
def getRooms(request,pk):
    # rooms = Room.objects.all()
    # serializer = RoomSerializer(rooms, many=True) # here we are using the RoomSerializer to convert the rooms object into a JSON object. The many=True argument is used to specify that we are serializing a queryset, not a single instance... many = True is use to serialize multiple objects
   
    # # here we are passing the rooms object to the Response... The response can't take python objects as arguments, so we have to convert the rooms object into a dictionary using the serializer...
    # return Response(serializer.data)

    room = Room.objects.get(id = pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)  # here we are passing the room object to the Response... The response can't take python objects as arguments, so we have to convert the room object into a dictionary using the serializer...
  


