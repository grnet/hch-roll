 #!/usr/bin/python
 # -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from roll.models import Establishment

from collections import defaultdict

import sys
import csv
import django
import re

VOTER_MAPPING = {
    (1, '5*****'): 1,
    (1, '4****'): 1,
    (1, '3***'): 1,
    (1, '2**'): 1,
    (1, '1*'): 1,
    (2, '5*****'): 2,
    (2, '4****'): 2,
    (2, '3***'): 2,
    (2, '2**'): 3,
    (2, '1*'): 3,
    (3, '5*****'): 4,
    (3, '4****'): 4,
    (3, '3***'): 4,
    (3, '2**'): 5,
    (3, '1*'): 5,
    (4, '5*****'): 6,
    (4, '4****'): 7,
    (4, '3***'): 8,
    (4, '2**'): 9,
    (4, '1*'): 10,
    (5, '5*****'): 11,
    (5, '4****'): 12,
    (5, '3***'): 13,
    (5, '2**'): 14,
    (5, '1*'): 15,
    (6, '5*****'): 16,
    (6, '4****'): 16,
    (6, '3***'): 16,
    (6, '2**'): 17,
    (6, '1*'): 17, 
    (7, '5*****'): 18,
    (7, '4****'): 19,
    (7, '3***'): 20,
    (7, '2**'): 21,
    (7, '1*'): 22,
    (8, '5*****'): 23,
    (8, '4****'): 24,
    (8, '3***'): 25,
    (8, '2**'): 26,
    (8, '1*'): 27,
    (9, '5*****'): 28,
    (9, '4****'): 28,
    (9, '3***'): 28,
    (9, '2**'): 28,
    (9, '1*'): 28,
    (10, '5*****'): 29,
    (10, '4****'): 29,
    (10, '3***'): 29,
    (10, '2**'): 29,
    (10, '1*'): 29,
    (11, '5*****'): 30,
    (11, '4****'): 30,
    (11, '3***'): 30,
    (11, '2**'): 30,
    (11, '1*'): 30,
    (12, u"Α'ΤΑΞΗΣ"): 31,
    (12, u"Β'ΤΑΞΗΣ"): 31,
    (12, u"Γ'ΤΑΞΗΣ"): 31,
    (12, u"Δ'ΤΑΞΗΣ"): 31,
    (12, u"Ε'ΤΑΞΗΣ"): 31,
}

VOTER_BALLOTS = defaultdict(list)

class Command(BaseCommand):
    help = """Extracts voters files"""
        
    def writenl(self, arg):
        self.stdout.write(arg)
        self.stdout.write("\n")

    def list_voters(self, args, options):
        if django.get_version() >= '1.5':
            write = self.stdout.write
        else:
            write = self.writenl
        establishments = Establishment.objects.select_related('voter',
                                                              'rating').filter(
            voter_id__isnull=False)

        for establishment in establishments:
            row = [
                establishment.registry_number,
                establishment.voter.email,
                establishment.voter.first_name,
                establishment.voter.surname,
                establishment.name,
                re.sub("[^0-9]", "", establishment.voter.mobile_phone),
            ]
            rating = establishment.rating.name
            key = (establishment.electoral_group.code, rating)
            if key not in VOTER_MAPPING:
                write("{0},{1},{2}".format(key[0], key[1].encode('utf-8'), establishment))
            else:
                ballot = VOTER_MAPPING[key]
		row.extend(key)
                urow = [c.encode('utf-8') if isinstance(c, basestring) else c
                       for c in row ]
                VOTER_BALLOTS[ballot].append(urow)
        for ballot in sorted(VOTER_BALLOTS.keys()):
            with open("ballot_{0}.csv".format(ballot), 'wb') as ballot_file:
                ballot_writer = csv.writer(ballot_file)
                for voter in VOTER_BALLOTS[ballot]:
                    ballot_writer.writerow(voter)

    def handle(self, *args, **options):
        self.list_voters(args, options)



