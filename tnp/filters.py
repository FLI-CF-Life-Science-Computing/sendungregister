import django_filters
from django_filters import FilterSet
from django.forms.widgets import CheckboxSelectMultiple
import django.forms
from .models import Address, Dataset, Profile, Disposal_type, Address

class DatasetFilter(FilterSet):
    class Meta:
        model = Dataset
        fields = ['category','date_of_disposal','added_by',]