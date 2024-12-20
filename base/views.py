from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from .models import Room , Topic
from django.shortcuts import get_object_or_404
from .forms import RoomForm
from django.db.models import Q
# Create your views here.



def home(request):
   q = request.GET.get('q') if request.GET.get('q') !=None else ''
   rooms = Room.objects.filter(
      Q(topic__name__icontains=q)|
      Q(name__icontains = q) |
      Q(description__icontains = q)
      )
   
   topics = Topic.objects.all()
   room_count = rooms.count()
   context = {'rooms': rooms ,'topics':topics , 'room_count': room_count}
   return render(request , 'base/home.html' ,context)
   # rooms = Room.objects.values()
   # if not rooms:
   #    message = {'message': 'no rooms found'}
   #    return JsonResponse(message , status=404)
   
   # context={'rooms': list(rooms)}
   # return JsonResponse(context)

def room(get, pk):
   # room = get_object_or_404(Room , id=pk)
   try:
      room = Room.objects.get(id = pk)
      context = {'room': room}
      return render(get , 'base/room.html', context)
   except Room.DoesNotExist:
      return HttpResponse("Room not found", status=404)
   # try:
   #    room = Room.objects.get(id = pk)
   #    room_data = {
   #       'id': room.id,
   #       'name': room.name,
   #       'description':room.description,
   #    }
   #    context ={'room': room_data}
   #    return JsonResponse(context , status=200)
   # except Room.DoesNotExist:
   #    error = {'error': 'Room not found'}
   #    return JsonResponse(error , status = 404)
def createRoom(request):
   form = RoomForm()
   if request.method == 'POST':
      print(request.POST)
      form =RoomForm(request.POST)
      if form.is_valid():
         form.save()
         return redirect('home')
   context ={'form': form}
   return render(request ,'base/room_form.html' , context )

def updateRoom(request , pk):
   room = Room.objects.get(id = pk)
   form = RoomForm(instance=room)
   if request.method == 'POST':
      print(request.POST)
      form =RoomForm(request.POST , instance=room)
      if form.is_valid():
         form.save()
         return redirect('home')
   context={'form':form}
   return render(request ,'base/room_form.html',context)

def deleteRoom(request , pk):
   room = Room.objects.get(id = pk)
   if request.method == 'POST':
      room.delete()
      return redirect('home')
   return render(request , 'base/delete.html', {'obj':room})