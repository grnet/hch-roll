from django.core.management.base import BaseCommand, CommandError

from roll.models import *

from collections import namedtuple
from datetime import datetime
import csv
import uuid

from django.db import transaction

ROW_HEADERS = [
    'registry_number',
    'name',
    'location',
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
]

class Command(BaseCommand):
    args = '<initial_data>.csv'
    help = 'Initialises the database'

    @transaction.commit_on_success
    def initialize_roll(self, datafile):
        RollRow = namedtuple('RollRow', ROW_HEADERS)
        for line, row in enumerate(
                map(lambda r: RollRow._make([s.decode('utf-8') for s in r]),
                    csv.reader(open(datafile, 'rb')))):
            registry_number = row.registry_number
            name = row.name
            location, c = Location.objects.get_or_create(name=row.location)
            if c:
                location.save()
            rating, c = Rating.objects.get_or_create(name=row.rating,
                                                     position=0)
            if c:
                rating.save()
            operator, c = Operator.objects.get_or_create(name=row.operator)
            if c:
                operator.save()
            owner, c = Owner.objects.get_or_create(name=row.owner)
            if c:
                owner.save()
            license = row.license
            if len(row.payment_date) > 0:
                payment_date = datetime.strptime(row.payment_date, '%m/%d/%Y')
                fee_payment, c = FeePayment.objects.get_or_create(
                    fee_paid=row.fee_paid,
                    payment_date=payment_date)
            else :
                fee_payment, c = FeePayment.objects.get_or_create(
                    fee_paid=row.fee_paid)
            if c:
                fee_payment.save()
            telephone = row.telephone
            fax = row.fax
            email = row.email
            electoral_group, c = ElectoralGroup.objects.get_or_create(
                code=row.electoral_group_code,
                name=row.electoral_group_name)
            if c:
                electoral_group.save()
            region, c = Region.objects.get_or_create(name=row.region)
            if c:
                region.save()
            prefecture, c = Prefecture.objects.get_or_create(
                name=row.prefecture,
                region=region)
            if c:
                prefecture.save()
            city, c = City.objects.get_or_create(name=row.city,
                                                 prefecture=prefecture)
            if c:
                city.save()
            island, c = Island.objects.get_or_create(name=row.island)
            if c:
                island.save()
            address, c = Address.objects.get_or_create(
                street_number=row.street_number,
                zip_code=row.zip_code,
                city=city,
                island=island,
                location=location)
            if c:
                address.save()
            establishment, c = Establishment.objects.get_or_create(
                registry_number=registry_number,
                name=name,
                address=address,
                rating=rating,
                operator=operator,
                owner=owner,
                license=license,
                fee_payment=fee_payment,
                telephone=telephone,
                fax=fax,
                email=email,
                electoral_group=electoral_group,
            )
            if c:
                establishment.unique_id = uuid.uuid4()
                establishment.save()
            self.stdout.write("\r{}".format(line), ending='')
            self.stdout.flush()
            line += 1
        self.stdout.write("")
        self.stdout.write("{}".format(line))                    
    
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("No input data file")
        else:
            self.initialize_roll(args[0])
    
