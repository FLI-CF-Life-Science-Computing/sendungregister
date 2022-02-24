from unicodedata import category
from django import forms
from .models import Dataset, Material, Book
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
from django.contrib.auth.models import User
from django_select2 import forms as s2forms


class AddressWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]

class AddDatasetForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super (AddDatasetForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['material'].queryset = Material.objects.filter(status="active").order_by('name')
        link_to_add_new_material = '<a href="/create/material" id="add_material" onclick="return showAddPopup(this);"><img src = "/static/admin/img/icon-addlink.svg"></a>'
        self.fields['material'].label = "Material {}".format(link_to_add_new_material)
        #self.fields['group'].queryset = Group.objects.filter(active=True).order_by('name')
        #link_to_add_new_group = '<a href="'+settings.SUBPATH+'/group/create" id="add_group" onclick="return showAddPopup(this);"><img src = "/static/admin/img/icon-addlink.svg" %}"></a>'
        #self.fields['group'].label = "Group {}".format(link_to_add_new_group)
        #self.fields['category'].queryset = ProjectCategory.objects.filter(active=True).order_by('name')
        #self.fields['associate'].queryset = HR.objects.filter(active=True).order_by('name')
        #self.fields['organism'].queryset = Organism.objects.filter(active=True).order_by('name')

    class Meta: 
        model = Dataset
        exclude = ('added_by','creation_date','lab')
        widgets = {
            'recipient': AddressWidget
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name',]

class AuthorWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "username__icontains",
        "email__icontains",
    ]


class CoAuthorsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "username__icontains",
        "email__icontains",
    ]


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        widgets = {
            "author": AuthorWidget,
            "co_authors": CoAuthorsWidget,
        }
