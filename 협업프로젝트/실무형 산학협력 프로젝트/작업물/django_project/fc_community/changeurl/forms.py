from django import forms
from .models import Url_content
from django.forms import ModelForm 

class Url_content_Form(ModelForm):
    class Meta:
        model = Url_content
        fields = ['site']