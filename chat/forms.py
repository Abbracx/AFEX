from django import forms
from django.forms import ModelForm
from .models import ChatMessage, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ChatMessageForm(ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={"class":"form", "rows":3, "placeholder":"Type messag here" }))
    class Meta:
        model = ChatMessage
        fields = ['body']

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields =  ['username', 'email', 'password1', 'password2']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name']