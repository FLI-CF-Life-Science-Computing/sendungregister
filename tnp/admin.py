from django.contrib import admin
from .models import Profile, Dataset, Lab, Address, Unit, Disposal_type,Specie,Material, Address
from simple_history.admin import SimpleHistoryAdmin 
from import_export.admin import ImportExportModelAdmin, ImportMixin, ExportMixin, ImportExportActionModelAdmin, ImportExportMixin
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

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

class DatasetExportResource(resources.ModelResource):
    pk = fields.Field(attribute='pk', column_name='ID')
    material__name = fields.Field(attribute='material__name', column_name='Material')
    article_number = fields.Field(attribute='article_number', column_name='Artikel-/Produktnummer')
    specie__name = fields.Field(attribute='specie__name', column_name='Tierart')
    category = fields.Field(attribute='category', column_name='Kategorie')
    amount = fields.Field(attribute='amount', column_name='Anzahl / Menge')
    unit__name = fields.Field(attribute='unit__name', column_name='Einheit')
    added_by__username = fields.Field(attribute='added_by__username', column_name='Zugefügt von')
    lab__name = fields.Field(attribute='lab__name', column_name='Gruppe/Lab')
    creation_date = fields.Field(attribute='creation_date', column_name='Erstellungsdatum')
    import_date = fields.Field(attribute='import_date', column_name='Importdatum')
    status = fields.Field(attribute='status', column_name='Status')
    sender = fields.Field(attribute='sender', column_name='Absender')
    sender_commercial = fields.Field(attribute='sender__commercial', column_name='Kommerzieller Absender')
    recipient = fields.Field(attribute='recipient', column_name='Empfänger')
    sender_recipient = fields.Field(attribute='recipient__commercial', column_name='Kommerzieller Empfänger')
    class Meta:
        model = Dataset
        fields = ('pk','material__name','article_number','specie__name','category','amount','unit__name','import_date','added_by__username','creation_date','status','lab__name','sender','sender_commercial','recipient','recipient_commercial')
        export_order = ('pk','material__name','specie__name','category','amount','unit__name','import_date','added_by__username','lab__name','creation_date','status','sender_commercial','recipient','recipient_commercial')

    def dehydrate_status(self, dataset):
        status = getattr(dataset, "status", "unknown")
        if status == 'c':
            status = 'closed'
        elif status == 'o':
            status = 'open'
        return status

    def dehydrate_sender(self, dataset):
        sender_name = getattr(dataset.sender, "name", "")
        sender_street = getattr(dataset.sender, "street", "")
        sender_plz = getattr(dataset.sender, "postal_code", "")
        sender_city = getattr(dataset.sender, "city", "")
        sender_country = getattr(dataset.sender, "country", "")
        return '%s, %s, %s %s, %s ' % (sender_name, sender_street, sender_plz, sender_city, sender_country)

    def dehydrate_recipient(self, dataset):
        recipient_name = getattr(dataset.recipient, "name", "")
        recipient_street = getattr(dataset.recipient, "street", "")
        recipient_plz = getattr(dataset.recipient, "postal_code", "")
        recipient_city = getattr(dataset.recipient, "city", "")
        recipient_country = getattr(dataset.recipient, "country", "")
        return '%s, %s, %s %s, %s ' % (recipient_name, recipient_street, recipient_plz, recipient_city, recipient_country)


@admin.register(Dataset)
class DatasetAdmin(ExportMixin, SimpleHistoryAdmin):
    list_display = ('pk','material', 'article_number','specie','category','amount','unit','point_of_origin','import_date','added_by','lab','creation_date','status')
    search_fields = ('material__name','specie__name','disposal_type__name','lab__name')
    def get_export_resource_class(self):
        return DatasetExportResource