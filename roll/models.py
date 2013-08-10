from django.db import models

from django.utils.translation import ugettext_lazy as _
import random
import string

random.seed()

class Location(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u"{}".format(self.name)

class Rating(models.Model):
    name = models.CharField(max_length=50)
    position = models.IntegerField()

    def __unicode__(self):
        return u"{} {}".format(self.name, self.position)

class Operator(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u"{}".format(self.name)

class Owner(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u"{}".format(self.name)


class FeePayment(models.Model):
    fee_paid = models.BooleanField()
    payment_date = models.DateField()

    class Meta:
        db_table  = 'roll_fee_payment'

    def __unicode__(self):
        return u"{} {:%d/%m/%Y}".format(self.fee_paid, self.payment_date)


class ElectoralGroup(models.Model):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)

    class Meta:
        db_table  =  'roll_electoral_group'

    def __unicode__(self):
        return u"{} {}".format(self.code, self.name)

class Region(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u"{}".format(self.name)

class Prefecture(models.Model):
    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region)

    def __unicode__(self):
        return u"{}".format(self.name, self.region)

class City(models.Model):
    name = models.CharField(max_length=200)
    prefecture = models.ForeignKey(Prefecture)

    def __unicode__(self):
        return u"{}".format(self.name, self.prefecture)

class Island(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return u"{}".format(self.name)

class Address(models.Model):
    street_number = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=20)
    city = models.ForeignKey(City)
    location = models.ForeignKey(Location)
    island = models.ForeignKey(Island)

    def __unicode__(self):
        return u"{} {} {} {} {}".format(self.street_number,
                                        self.zip_code,
                                        self.city,
                                        self.location,
                                        self.island)

class Voter(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    mobile_phone = models.CharField(max_length=20)

    def __unicode__(self):
        return u"{} {} {}".format(self.name, self.email, self.mobile_phone)

class Establishment(models.Model):
    registry_number = models.IntegerField(unique=True,
                                          verbose_name=_("registry number"))
    name = models.CharField(max_length=200,
                            verbose_name=_("name"))
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

    def __unicode__(self):
        return u"{} {} {}".format(self.registry_number, self.name,
                                  self.address)

