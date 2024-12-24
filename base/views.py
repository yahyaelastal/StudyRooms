from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Room , Topic , Message
from .forms import RoomForm , MessageForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def loginPage(request):

   if request.user.is_authenticated:
      return redirect('home')

   if request.method == 'POST':
      username= request.POST.get('username').lower()
      password= request.POST.get('password')

      try:
         user = User.objects.get(username = username)
      except:
         messages.error(request, 'User doesnt exist')

      user = authenticate(request , username=username , password= password)
      if user is not None:
         login(request , user)
         return redirect('home')
      else:
         messages.error(request, 'username OR password doesnt exist')


   context = {'page' : 'login'}
   return render(request, 'base/login_register.html', context)

def logoutUser(request):
   logout(request)
   return redirect('home')

def registerUser(request):
   form = UserCreationForm()
   if request.method == 'POST':
      form = UserCreationForm(request.POST)
      if form.is_valid():
         user = form.save(commit=False)
         user.username = user.username.lower()
         user.save()
         login(request, user)
         return redirect('home')
      else:
         messages.error(request , 'An error occured during registration')
   context = {'form': form}
   return render(request , 'base/login_register.html', context)


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
     

def room(request, pk):
   try:
      room = Room.objects.get(id = pk)
      room_messages = room.message_set.all().order_by('-created')
      participants = room.participants.all()
      context = {'room': room , 'room_messages': room_messages , 'participants':participants}
      if request.method == 'POST':
         message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
         )
         room.participants.add(request.user)
         return redirect('room', pk=room.id)
      return render(request , 'base/room.html', context)
   except Room.DoesNotExist:
      return HttpResponse("Room not found", status=404)

@login_required(login_url = '/login' )
def createRoom(request):
   form = RoomForm()
   if request.method == 'POST':
      print(request.POST)
      form =RoomForm(request.POST)
      if form.is_valid():
         room = form.save(commit=False)
         room.host = request.user
         room.save()
         return redirect('home')
   context ={'form': form}
   return render(request ,'base/form.html' , context )

@login_required(login_url = '/login' )
def updateRoom(request , pk):
   room = Room.objects.get(id = pk)
   form = RoomForm(instance=room)

   if request.user != room.host :
      return HttpResponse('You are not allowed here')
   if request.method == 'POST':
      print(request.POST)
      form =RoomForm(request.POST , instance=room)
      if form.is_valid():
         form.save()
         return redirect('home')
   context={'form':form}
   return render(request ,'base/form.html',context)

@login_required(login_url = '/login' )
def deleteRoom(request , pk):
   room = Room.objects.get(id = pk)

   if request.user != room.host :
      return HttpResponse('You are not allowed here')
   if request.method == 'POST':
      room.delete()
      return redirect('home')
   return render(request , 'base/delete.html', {'obj':room})

@login_required(login_url = '/login' )
def updateMessage(request , pk):
   message = Message.objects.get(id = pk)
   form = MessageForm(instance=message)
   if request.user != message.user:
      return HttpResponse('You are not allowed here')
   
   if request.method =='POST':
      form = MessageForm(request.POST , instance=message)
      if form.is_valid():
         form.save()
         return redirect('room', pk=message.room.id)
   context = {'form': form}
   return render(request , 'base/form.html', context)

@login_required(login_url = '/login' )
def deleteMessage(request , pk):
   message = Message.objects.get(id = pk)
   if request.user != message.user:
      return HttpResponse('You are not allowed here')
   
   if request.method == 'POST':
      message.delete()
      return redirect('room', pk=message.room.id)
   
   return render(request , 'base/delete.html', {'obj':message})