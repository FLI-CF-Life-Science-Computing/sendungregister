from django.contrib import admin
from .models import Profile, Dataset, Lab, Address, Unit, Disposal_type,Specie,Material 


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('user__username','lab__name')

@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    search_fields = ('name','status')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    search_fields = ('name','status')

@admin.register(Specie)
class SpecieAdmin(admin.ModelAdmin):
    search_fields = ('name','status')


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    search_fields = ('name','status')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    search_fields = ('name','street','postal_code','city')

@admin.register(Disposal_type)
class Disposal_typeAdmin(admin.ModelAdmin):
    search_fields = ('name','street','postal_code','city')

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ('material','specie','category','amount','unit','point_of_origin','added_by','lab','creation_date','status')
    search_fields = ('material__name','specie__name','disposal_type__name','lab__name')