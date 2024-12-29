from django import forms
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User
from .models import post

class signupform(UserCreationForm):
    class Meta:
        model = User
        fields = ["username" , "first_name" , "last_name" , "email"]
        labels = {"email" : "Email"}
        
        
 
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        }),
        label="Username"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        }),
        label="Password"
    )
    
class PostForm(forms.ModelForm):
    class Meta:
        model = post
        fields = ["title" , "description"]
        labels = {"title :TITLE"  , "description : description"}          