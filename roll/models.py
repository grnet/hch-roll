from django.db import models

import random
import string

random.seed()

class Location(models.Model):
    name = models.CharField(max_length=200)

class Rating(models.Model):
    name = models.CharField(max_length=50)
    position = models.IntegerField()

class Operator(models.Model):
    name = models.CharField(max_length=200)

class Owner(models.Model):
    name = models.CharField(max_length=200)

class FeePayment(models.Model):
    fee_paid = models.BooleanField()
    payment_date = models.DateField()

    class Meta:
        db_table  = 'roll_fee_payment'

class ElectoralGroup(models.Model):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)

    class Meta:
        db_table  =  'roll_electoral_group'

class Region(models.Model):
    name = models.CharField(max_length=200)

class Prefecture(models.Model):
    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region)
    
class City(models.Model):
    name = models.CharField(max_length=200)
    prefecture = models.ForeignKey(Prefecture)

class Island(models.Model):
    name = models.CharField(max_length=100)
    
class Address(models.Model):
    street_number = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=20)
    city = models.ForeignKey(City)
    island = models.ForeignKey(Island)

class Voter(models.Model):
    name = models.CharField(max_length=200)
    e_mail = models.EmailField()
    mobile_phone = models.CharField(max_length=20)
    
class Establishment(models.Model):
    registry_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    location = models.ForeignKey(Location)
    rating = models.ForeignKey(Rating)
    operator = models.ForeignKey(Operator)
    owner = models.ForeignKey(Owner)
    license = models.BooleanField()
    fee_payment = models.ForeignKey(FeePayment,
                                    related_name='fee_payment')
    telephone = models.CharField(max_length=20)
    fax = models.CharField(max_length=20)
    email = models.EmailField()
    electoral_group = models.ForeignKey(ElectoralGroup,
                                        related_name='electoral_group')
    voter = models.ForeignKey(Voter, null=True, blank=True)
    unique_id = models.CharField(max_length=200, unique=True)

    
