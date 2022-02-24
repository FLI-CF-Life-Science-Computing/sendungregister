from unicodedata import category
from django import forms
from .models import Address, Dataset, Material, Book
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
from django.contrib.auth.models import User
from django_select2 import forms as s2forms


class AddressWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]

class AddressWidget2(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]

class AddDatasetForm(forms.ModelForm):
    date_of_disposal     = forms.DateField(input_formats=['%d/%m/%Y'],required=False)

    def __init__(self,*args,**kwargs):
        super (AddDatasetForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['material'].queryset = Material.objects.filter(status="active").order_by('name')
        link_to_add_new_material = '<a href="/create/material" id="add_material" onclick="return showAddPopup(this);"><img src = "/static/admin/img/icon-addlink.svg"></a>'
        self.fields['material'].label = "Material {}".format(link_to_add_new_material)

        self.fields['point_of_origin'].queryset = Address.objects.filter(status="active").order_by('name')
        link_to_add_new_address = '<a href="/create/origin_address" id="add_address" onclick="return showAddPopup(this);"><img src = "/static/admin/img/icon-addlink.svg"></a>'
        self.fields['point_of_origin'].label = "Point of origin {}".format(link_to_add_new_address)

        self.fields['sender'].queryset = Address.objects.filter(status="active").order_by('name')
        link_to_add_new_address = '<a href="/create/sender_address" id="add_sender" onclick="return showAddPopup(this);"><img src = "/static/admin/img/icon-addlink.svg"></a>'
        self.fields['sender'].label = "Sender {}".format(link_to_add_new_address)

        self.fields['recipient'].queryset = Address.objects.filter(status="active").order_by('name')
        link_to_add_new_address = '<a href="/create/recipient_address" id="add_recipient" onclick="return showAddPopup(this);"><img src = "/static/admin/img/icon-addlink.svg"></a>'
        self.fields['recipient'].label = "Recipient {}".format(link_to_add_new_address)


    class Meta: 
        model = Dataset
        exclude = ('added_by','creation_date','lab')
        widgets = {
            'recipient': AddressWidget,
            'point_of_origin':AddressWidget,
            'sender':AddressWidget2,
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name',]

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('status',)
