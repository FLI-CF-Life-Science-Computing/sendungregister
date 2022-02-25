from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings

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
    name        = models.CharField(max_length=200)
    street      = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    city        = models.CharField(max_length=30)
    status = models.CharField(max_length=50, choices=(
        ('active', 'active'),
        ('deactivated', 'deactivated'),
        ),default='active')
    #address = models.ForeignKey(Address, null=False, on_delete=models.CASCADE)
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
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ),default='3')    
    amount              = models.DecimalField(max_digits=10, decimal_places=2, help_text='Menge')
    unit                = models.ForeignKey(Unit, null=False, blank=False, help_text='Einheit', on_delete=models.CASCADE)
    point_of_origin     = models.ForeignKey(Address, null=False, blank=False, on_delete=models.CASCADE, help_text='Herkunftsort', related_name='origin_address')
    sender              = models.ForeignKey(Address, null=False, blank=False, on_delete=models.CASCADE, help_text='Absender', related_name='sender_address')
    recipient           = models.ForeignKey(Address, null=False, blank=False, on_delete=models.CASCADE, help_text='Empfänger', related_name='recipient_address')
    prospective_date_of_disposal = models.DateField(null=True, blank=True)
    date_of_disposal    = models.DateField(null=True, blank=True, help_text='Entsorgungsdatum')
    disposal_type       = models.ForeignKey(Disposal_type, null=True, blank=True, help_text='Entsorgungsart', on_delete=models.CASCADE)
    added_by            = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    creation_date       = models.DateTimeField(null=False, auto_now_add=True)
    lab                 = models.ForeignKey(Lab, null=False, blank=False, on_delete=models.CASCADE)
    status              = models.CharField(max_length=2, choices=(
        ('o', 'open'),
        ('c', 'closed'),
        ),default='o')  
    
    def save(self, *args, **kwargs):
        if self.disposal_type & self.date_of_disposal: 
            self.status = 'c'
        else:
            self.status = 'o'
            
        return super(Dataset, self).save(*args, **kwargs)

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


