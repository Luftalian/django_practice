from django import forms
from .models import Photos, User, Comment

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photos
        fields = ['title', 'image', 'text', 'user']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'avatar']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
