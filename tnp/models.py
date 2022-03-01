from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings
from simple_history.models import HistoricalRecords
from django.core.mail import send_mail


class Lab(models.Model):

    name = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    def __str__(self):
        return self.name + ' Lab'

class Material(models.Model):

    name = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if not self.pk: 
            admin_mail = getattr(settings, "ADMIN_EMAIL", None)
            inform_about_new_material = getattr(settings, "INFORM_ABOUT_NEW_MATERIAL", False)
            if inform_about_new_material:
                send_mail("Sendungsregister: Neues Material {}".format(self.name),"Neues Material {}".format(self.name), "sendungsregister@leibniz-fli.de",[admin_mail])
        return super(Material, self).save(*args, **kwargs)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __str__(self):
        return self.name

class Specie(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    def __str__(self):
        return self.name

#class Address(models.Model):
#    name        = models.CharField(max_length=30)
#    street      = models.CharField(max_length=200)
#    postal_code = models.CharField(max_length=10)
#    city        = models.CharField(max_length=30)
#    def __str__(self):
#        return self.name

class Address(models.Model):
    name        = models.CharField(max_length=200, help_text='Name')
    street      = models.CharField(max_length=200, help_text='Straße')
    postal_code = models.CharField(max_length=10, help_text='PLZ')
    city        = models.CharField(max_length=30, help_text='Stadt')
    country     = models.CharField(max_length=30, help_text='Land', default='Deutschland')
    status = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    history = HistoricalRecords()
    #address = models.ForeignKey(Address, null=False, on_delete=models.CASCADE)

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __str__(self):
        return "{}, {}, {}, {}".format(self.name,self.street,self.postal_code,self.city)


class Disposal_type(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    def __str__(self):
        return self.name

class Dataset(models.Model):
    material            = models.ForeignKey(Material, null=False, blank=False, help_text='Material', on_delete=models.CASCADE)
    specie              = models.ForeignKey(Specie, null=False, blank=False, help_text='Tierart', on_delete=models.CASCADE)
    category            = models.CharField(max_length=2, help_text='Kategorie', choices=(
        ('1', '1 - high risk / hohes Risiko '),
        ('2', '2 - moderate risk / mittleres Risiko'),
        ('3', '3 - low risk / geringes Risiko'),
        ),default='3')    
    amount              = models.DecimalField(max_digits=10, decimal_places=2, help_text='Menge')
    unit                = models.ForeignKey(Unit, null=False, blank=False, help_text='Einheit', on_delete=models.CASCADE)
    point_of_origin     = models.ForeignKey(Address, null=False, blank=False, on_delete=models.CASCADE, help_text='Herstellungsort', related_name='origin_address')
    sender              = models.ForeignKey(Address, null=False, blank=False, on_delete=models.CASCADE, help_text='Absender', related_name='sender_address')
    recipient           = models.ForeignKey(Address, null=False, blank=False, on_delete=models.CASCADE, help_text='Empfänger', related_name='recipient_address')
    reminder_disposal = models.DateField(null=True, blank=True)
    date_of_disposal    = models.DateField(null=True, blank=True, help_text='Entsorgungsdatum')
    disposal_type       = models.ForeignKey(Disposal_type, null=True, blank=True, help_text='Entsorgungsart', on_delete=models.CASCADE)
    added_by            = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    creation_date       = models.DateTimeField(null=False, auto_now_add=True)
    lab                 = models.ForeignKey(Lab, null=False, blank=False, on_delete=models.CASCADE)
    status              = models.CharField(max_length=2, choices=(
        ('o', 'open'),
        ('c', 'closed'),
        ),default='o')
    history = HistoricalRecords() 
        
    def save(self, *args, **kwargs):
        if self.disposal_type and self.date_of_disposal: 
            self.status = 'c'
        else:
            self.status = 'o'
        return super(Dataset, self).save(*args, **kwargs)
    
    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lab  = models.ForeignKey(Lab, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

class Book(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    co_authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='co_authored_by')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


