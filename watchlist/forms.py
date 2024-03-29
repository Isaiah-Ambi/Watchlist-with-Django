from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Show, WatchListShow, CustomList

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User  # Your custom User model if you have one
        fields = ['username', 'email', 'password1', 'password2']

class NewShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = ['tvmaze_id', 'name', 'genres', 'status', 'image_url', 'premiered', 'rating', 'summary']

class WatchListShowForm(forms.ModelForm):
    class Meta:
        model = WatchListShow
        fields = ['watch_status']

class CustomListForm(forms.ModelForm):
    class Meta:
        model = CustomList
        fields = ['name']

