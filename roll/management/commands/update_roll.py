from django.core.management.base import BaseCommand, CommandError

from roll.models import *

from collections import namedtuple
from datetime import datetime
import csv
import django
import re

from functools import partial

from django.db import transaction

ROW_HEADER = [
    'registry_number',
    'name',
    'location',
    'establishment_type',
    'rating',
    'operator',
    'owner',
    'license',
    'fee_paid',
    'payment_date',
    'telephone',
    'fax',
    'email',
    'electoral_group_code',
    'electoral_group_name',
    'prefecture',
    'region',
    'island',
    'street_number',
    'zip_code',
    'city',
    'voter_first_name',
    'voter_surname',
    'voter_email',
    'voter_mobile_phone',
]

class Command(BaseCommand):
    args = '<update_data_csv_file>'
    help = 'Updates the database'
    
    @transaction.commit_on_success
    def update_roll(self, datafile):
        if django.get_version() >= '1.5':
            write = partial(self.stdout.write, ending = '')
        else:
            write = self.stdout.write
        RollRow = namedtuple('RollRow', ROW_HEADER)
        for line, row in enumerate(
                map(lambda r: RollRow._make([s.decode('utf-8') for s in r]),
                    csv.reader(open(datafile, 'rb')))):
            if line == 0:
                continue
            registry_number = row.registry_number
            name = row.name
            location, c = Location.objects.get_or_create(name=row.location)
            establishment_type, c = EstablishmentType.objects.get_or_create(
                name=row.establishment_type)
            rating, c = Rating.objects.get_or_create(name=row.rating,
                                                     position=0)
            operator, c = Operator.objects.get_or_create(name=row.operator)
            owner, c = Owner.objects.get_or_create(name=row.owner)
            license = row.license
            if row.fee_paid == 'True':
                fee_paid = True
            else:
                fee_paid = False
            if len(row.payment_date) > 0:
                payment_date = datetime.strptime(row.payment_date, '%Y-%m-%d')
                fee_payment, c = FeePayment.objects.get_or_create(
                    fee_paid=fee_paid,
                    payment_date=payment_date)
            else :
                fee_payment, c = FeePayment.objects.get_or_create(
                    fee_paid=fee_paid)
            telephone = row.telephone
            fax = row.fax
            email = row.email
            electoral_group, c = ElectoralGroup.objects.get_or_create(
                code=row.electoral_group_code,
                name=row.electoral_group_name)
            region, c = Region.objects.get_or_create(name=row.region)
            prefecture, c = Prefecture.objects.get_or_create(
                name=row.prefecture,
                region=region)
            city, c = City.objects.get_or_create(name=row.city,
                                                 prefecture=prefecture)
            island, c = Island.objects.get_or_create(name=row.island)
            address, c = Address.objects.get_or_create(
                street_number=row.street_number,
                zip_code=row.zip_code,
                city=city,
                island=island,
                location=location)
            establishment, c = Establishment.objects.get_or_create(
                registry_number=registry_number)
            establishment.name = name
            establishment.establishment__type = establishment_type
            establishment.address = address
            establishment.rating = rating
            establishment.operator = operator
            establishment.owner = owner
            establishment.license = license
            establishment.fee_payment = fee_payment
            establishment.telephone = telephone
            establishment.fax = fax
            establishment.email = email
            establishment.electoral_group = electoral_group
            if c:
                establishment.unique_id = Establishment.generate_unique_id()
            if establishment.voter_id is None:
                voter = Voter()
            else:
                voter = establishment.voter
            voter.first_name = row.voter_first_name
            voter.surname = row.voter_surname
            voter.email = row.voter_email
            voter.mobile_phone=re.sub("[^0-9]", "", row.voter_mobile_phone)
            voter.save()
            if establishment.voter_id is None:
                establishment.voter = voter                
            establishment.save()
            write("\r{0}".format(line+1))
            self.stdout.flush()            
        write("\n")

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("No input data file")
        else:
            self.update_roll(args[0])

