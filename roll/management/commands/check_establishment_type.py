from django.core.management.base import BaseCommand, CommandError

from roll.models import *

from collections import namedtuple
import csv

from optparse import make_option

from django.db import transaction

ROW_HEADERS = [
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
]

class Command(BaseCommand):
    args = '<initial_data_csv_file>'
    help = 'Checks the establishment type'
    option_list = BaseCommand.option_list + (
        make_option('-f',
                    '--fix',
                    action='store_true',
                    dest='fix',
                    default=False,
                    help='Fix differences',
                ),        
    )
    
    @transaction.commit_on_success
    def check_establishment_type(self, datafile, options):
        RollRow = namedtuple('RollRow', ROW_HEADERS)
        for line, row in enumerate(
                map(lambda r: RollRow._make([s.decode('utf-8') for s in r]),
                    csv.reader(open(datafile, 'rb')))):
            registry_number = row.registry_number
            et = EstablishmentType.objects.get(name=row.establishment_type)
            e = Establishment.objects.get(registry_number=registry_number)
            if et != e.establishment_type:
                e_et_name = e.establishment_type.name
                et_name = et.name
                self.stdout.write(u"{0} {1} {2} {3}".format(line+1,
                                                            registry_number,
                                                            e_et_name,
                                                            et_name))
                if options['fix']:
                    e.establishment_type = et
                    e.save()
                self.stdout.flush()

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("No input data file")
        else:
            self.check_establishment_type(args[0], options)

