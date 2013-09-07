from django.db import models

from django.utils.translation import ugettext_lazy as _

import random
import string

random.seed()

class Location(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u"{0}".format(self.name)

class Rating(models.Model):
    name = models.CharField(max_length=50)
    position = models.IntegerField()

    def __unicode__(self):
        return u"{0}".format(self.name)

class Operator(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u"{0}".format(self.name)

class Owner(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u"{0}".format(self.name)


class FeePayment(models.Model):
    fee_paid = models.BooleanField()
    payment_date = models.DateField()

    class Meta:
        db_table  = 'roll_fee_payment'

    def __unicode__(self):
        return u"{0} {1:%d/%m/%Y}".format(self.fee_paid, self.payment_date)


class ElectoralGroup(models.Model):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)

    class Meta:
        db_table  =  'roll_electoral_group'

    def __unicode__(self):
        return u"{0} {1}".format(self.code, self.name)

class Region(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u"{0}".format(self.name)

class Prefecture(models.Model):
    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region)

    def __unicode__(self):
        return u"{0} {1}".format(self.name, self.region)

class City(models.Model):
    name = models.CharField(max_length=200)
    prefecture = models.ForeignKey(Prefecture)

    def __unicode__(self):
        return u"{0} {1}".format(self.name, self.prefecture)

class Island(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return u"{0}".format(self.name)

class Address(models.Model):
    street_number = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=20)
    city = models.ForeignKey(City)
    location = models.ForeignKey(Location)
    island = models.ForeignKey(Island)

    def __unicode__(self):
        return u"{0} {1} {2} {3} {4}".format(self.street_number,
                                             self.zip_code,
                                             self.city,
                                             self.location,
                                             self.island)

class Voter(models.Model):
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_phone = models.CharField(max_length=20)

    def __unicode__(self):
        return u"{0} {1} {2}".format(self.name, self.email, self.mobile_phone)

class EstablishmentType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return u"{0}".format(self.name)
    
    class Meta:
        db_table  = 'roll_establishment_type'

class Establishment(models.Model):
    registry_number = models.IntegerField(unique=True,
                                          verbose_name=_("registry number"))
    name = models.CharField(max_length=200,
                            verbose_name=_("name"))
    establishment_type = models.ForeignKey(EstablishmentType,
                                           verbose_name=_("establishment type"))
    address = models.ForeignKey(Address,
                                verbose_name=_("address"))
    rating = models.ForeignKey(Rating,
                               verbose_name=_("rating"))
    operator = models.ForeignKey(Operator,
                                 verbose_name=_("operator"))
    owner = models.ForeignKey(Owner,
                              verbose_name=_("owner"))
    license = models.BooleanField(verbose_name=_("license"))
    fee_payment = models.ForeignKey(FeePayment,
                                    related_name='fee_payment',
                                    verbose_name=_("fee payment"))
    telephone = models.CharField(max_length=20,
                                 verbose_name=_("telephone"))
    fax = models.CharField(max_length=20,
                           verbose_name=_("fax"))
    email = models.EmailField(verbose_name=_("email"))
    electoral_group = models.ForeignKey(ElectoralGroup,
                                        related_name='electoral_group',
                                        verbose_name=_("electoral group"))
    voter = models.ForeignKey(Voter, null=True, blank=True,
                              verbose_name=_("voter"))
    unique_id = models.CharField(max_length=200, unique=True,
                                 verbose_name=_("unique id"))

    @classmethod
    def generate_random_id(cls):
        pieces = [''.join(random.choice(string.digits) for x in range(4))
                  for x in range(0, 4)]
        return '-'.join(pieces)
        
    @classmethod
    def generate_unique_id(cls):
        unique_id = Establishment.generate_random_id()
        while Establishment.objects.filter(unique_id=unique_id).exists():
            unique_id = Establishment.generate_random_id()
        return unique_id

    def reset_unique_id(self):
        self.unique_id = Establishment.generate_unique_id()
        
    def __unicode__(self):
        return u"{0} {1} {2} {3}".format(self.registry_number,
                                         self.name,
                                         self.establishment_type,
                                         self.address)

