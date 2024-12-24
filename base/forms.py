from django.forms import ModelForm
from .models import Room , Message

class RoomForm(ModelForm):
    class Meta:
        model = Room
        exclude = ['host']

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body'] 