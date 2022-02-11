from django.db import models

class Lab(models.Model):

    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name + ' Lab'

class Material(models.Model):

    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Specie(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Disposal_type(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Dataset(models.Model):
    category = models.CharField(max_length=2, choices=(
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ),default='3')
    amount  = models.PositiveIntegerField()
    unit    =  models.ForeignKey(Unit, null=False, on_delete=models.CASCADE)
    date_of_disposal = models.DateField(null=True, blank=True)


