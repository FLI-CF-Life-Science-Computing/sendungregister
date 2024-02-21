from unicodedata import category
from django import forms
from .models import Address, Dataset, Material, Specie, Unit
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import datetime
from django.contrib.auth.models import User
from django_select2 import forms as s2forms
from html import escape


class AddressWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]

class AddressWidget2(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]

class AddDatasetForm(forms.ModelForm):
    #date_of_disposal     = forms.DateField(input_formats=['%d/%m/%Y'],required=False)
    reminder_disposal = forms.DateField(input_formats=['%d/%m/%Y'],required=False, help_text='Datum für Erinnerungsmail zum Eintragen des Entsorgungsdatum')
    field_order = ['material', 'specie', 'category','unit','amount','point_of_origin','sender','recipient']
    material = forms.ModelChoiceField(queryset=Material.objects.filter(status='active').order_by('name'))
    specie = forms.ModelChoiceField(queryset=Specie.objects.filter(status='active').order_by('name'))
    unit = forms.ModelChoiceField(queryset=Unit.objects.filter(status='active').order_by('name'))
    import_date = forms.DateField(input_formats=['%d/%m/%Y'],required=False, help_text='Importdatum')
    field_order = ['material','article_number', 'specie', 'category','unit','amount','point_of_origin','sender','recipient','import_date','prospective_date_of_disposal','date_of_disposal','disposal_type']

    def __init__(self,*args,**kwargs):
        super (AddDatasetForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['material'].queryset = Material.objects.filter(status="active").order_by('name')
        link_to_add_new_material ='<a href="/create/material" id="add_material" onclick="return showAddPopup(this);"><img src = "/static/admin/img/icon-addlink.svg"></a>'
        self.fields['material'].label = "Material  {}".format(link_to_add_new_material)
        self.fields['material'].label = "Material"

        self.fields['point_of_origin'].queryset = Address.objects.filter(status="active").order_by('name')
        link_to_add_new_address = '<a href="/create/origin_address" id="add_address" onclick="return showAddPopup(this);"><img src = "/static/admin/img/icon-addlink.svg"></a>'
        self.fields['point_of_origin'].label = "Point of origin {}".format(link_to_add_new_address)
        self.fields['point_of_origin'].label = "Point of origin"

        self.fields['sender'].queryset = Address.objects.filter(status="active").order_by('name')
        link_to_add_new_address = '<a href="/create/sender_address" id="add_sender" onclick="return showAddPopup(this);"><img src = "/static/admin/img/icon-addlink.svg"></a>'
        self.fields['sender'].label = "Sender {}".format(link_to_add_new_address)
        self.fields['sender'].label = "Sender"

        self.fields['recipient'].queryset = Address.objects.filter(status="active").order_by('name')
        link_to_add_new_address = '<a href="/create/recipient_address" id="add_recipient" onclick="return showAddPopup(this);"><img src = "/static/admin/img/icon-addlink.svg"></a>'
        self.fields['recipient'].label = "Recipient {}".format(link_to_add_new_address)
        self.fields['recipient'].label = "Recipient"

        link_to_category_definition = '<a href="https://www.bmel.de/DE/themen/tiere/tiergesundheit/tierische-nebenprodukte/tierische-nebenprodukte-kategorie.html" target="_blank">Info</a>'
        self.fields['category'].label = "Category ({})".format(link_to_category_definition)
        self.fields['category'].label = "Category"

    class Meta: 
        model = Dataset
        exclude = ('added_by','creation_date','lab','date_of_disposal','disposal_type','status')
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


class DatasetEditForm(forms.ModelForm):
    reminder_disposal = forms.DateField(widget=forms.widgets.DateInput(format="%d/%m/%Y"),input_formats=['%d/%m/%Y'],required=False, help_text='Datum für Erinnerungsmail zum Eintragen des Entsorgungsdatum')
    date_of_disposal     = forms.DateField(widget=forms.widgets.DateInput(format="%d/%m/%Y"),input_formats=['%d/%m/%Y'],required=False, help_text='Entsorgungsdatum')
    import_date     = forms.DateField(widget=forms.widgets.DateInput(format="%d/%m/%Y"),input_formats=['%d/%m/%Y'],required=False, help_text='Importdatum')
    field_order = ['material','article_number', 'specie', 'category','unit','amount','point_of_origin','sender','recipient','import_date','prospective_date_of_disposal','date_of_disposal','disposal_type']
    def __init__(self,*args,**kwargs):
        super (DatasetEditForm,self ).__init__(*args,**kwargs) # populates the post
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
    
    #def __init__(self,*args,**kwargs):
    #    super (DatasetEditForm,self ).__init__(*args,**kwargs)
    #    self.fields['material'].disabled = True
    #    self.fields['specie'].disabled = True
    #    self.fields['category'].disabled = True
    #    self.fields['unit'].disabled = True
    #    self.fields['amount'].disabled = True
    #    self.fields['point_of_origin'].disabled = True
    #    self.fields['sender'].disabled = True
    #    self.fields['recipient'].disabled = True
    class Meta: 
        model = Dataset
        exclude = ('added_by','creation_date','lab','status')
        widgets = {
            'recipient': AddressWidget,
            'point_of_origin':AddressWidget,
            'sender':AddressWidget2,
        }
