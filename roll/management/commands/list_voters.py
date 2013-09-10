from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from roll.models import Voter

import sys
import csv

class Command(BaseCommand):
    help = """Shows list of voters"""
        
    def list_voters(self, args, options):
        voters = Voter.objects.all()
        voter_writer = csv.writer(sys.stdout)
        for voter in voters:
            for establishment in voter.establishment_set.all():
                row = [
                    establishment.registry_number,
                    establishment.name,
                    establishment.address.location.name,
                    establishment.establishment_type.name,
                    establishment.rating.name,
                    establishment.operator.name,
                    establishment.owner.name,
                    establishment.license,
                    establishment.fee_payment.fee_paid,
                    establishment.fee_payment.payment_date,
                    establishment.telephone,
                    establishment.fax,
                    establishment.email,
                    establishment.electoral_group.code,
                    establishment.electoral_group.name,
                    establishment.address.city.prefecture.name,
                    establishment.address.city.prefecture.region.name,
                    establishment.address.island,
                    establishment.address.street_number,
                    establishment.address.zip_code,
                    establishment.address.city,
                    voter.first_name,
                    voter.surname,
                    voter.email,
                    voter.mobile_phone
                ]
                print row
                urow = [c.encode('utf-8') if isinstance(c, basestring) else c
                        for c in row ]
                voter_writer.writerow(urow)
        

    def handle(self, *args, **options):
        self.list_voters(args, options)



