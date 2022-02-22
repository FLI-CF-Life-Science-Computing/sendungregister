from unicodedata import category
from django import forms
from .models import Dataset
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
from django.contrib.auth.models import User

class AddDatasetForm(forms.ModelForm):
    class Meta: 
        model = Dataset
        exclude = ('added_by','creation_date','lab')
