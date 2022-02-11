from django.contrib import admin
from .models import Profile, Dataset, Lab, Address, Unit, Disposal_type,Specie,Material 


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__username','lab__name')

@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    search_fields = ('name','status')