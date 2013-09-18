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

# 1: 5
# 2: 2
# 3: 2
# 4: 4
# 5: 5
# 6: 2
# 7: 5
# 8: 5
# 9: 1
# 10: 1
# 11: 1
# 12: 1

GROUPS = {
    1: "1η (Στερεά Ελλάδα - Εύβοια – Αργοσαρωνικός - Κύθηρα)",
    2: "2η (Πελλοπόνησος - Ελαφόνησος)",
    3: "3η (Θεσσαλία - Σποράδες - Σκύρος)",
    4: "4η (Ιόνια Νησιά)",
    5: "5η (Μακεδονία - Θράκη - Θάσος)",
    6: "6η (Κυκλάδες)",
    7: "7η (Κρήτη)",
    8: "8η (Δωδεκάνησα)",
    9: "9η (Ήπειρος)",
    10: "10η (Νησιά Βορείου Αιγαίου)",
    11: "11η (Λουτροπόλεις)",
    12: "12η (Κάμπινγκ)",
}

ELECTION_NAMES = {
    1: "5 Αστέρων - Ομάδα %s" % GROUPS[1],
    2: "4 Αστέρων - Ομάδα %s" % GROUPS[1],
    3: "3 Αστέρων - Ομάδα %s" % GROUPS[1],
    4: "2 Αστέρων - Ομάδα %s" % GROUPS[1],
    5: "1 Αστέρος - Ομάδα %s" % GROUPS[1],

    6: "5,4,3 Αστέρων - Ομάδα %s" % GROUPS[2],
    7: "2,1 Αστέρων - Ομάδα %s" % GROUPS[2],

    8: "5,4,3 Αστέρων - Ομάδα %s" % GROUPS[3],
    9: "2,1 Αστέρων - Ομάδα %s" % GROUPS[3],

    10: "5 Αστέρων - Ομάδα %s" % GROUPS[4],
    11: "4 Αστέρων - Ομάδα %s" % GROUPS[4],
    12: "3 Αστέρων - Ομάδα %s" % GROUPS[4],
    13: "2,1 Αστέρων - Ομάδα %s" % GROUPS[4],

    14: "5 Αστέρων - Ομάδα %s" % GROUPS[5],
    15: "4 Αστέρων - Ομάδα %s" % GROUPS[5],
    16: "3 Αστέρων - Ομάδα %s" % GROUPS[5],
    17: "2 Αστέρων - Ομάδα %s" % GROUPS[5],
    18: "1 Αστέρος - Ομάδα %s" % GROUPS[5],

    19: "5,4,3 Αστέρων - Ομάδα %s" % GROUPS[6],
    20: "2,1 Αστέρων - Ομάδα %s" % GROUPS[6],

    21: "5 Αστέρων - Ομάδα %s" % GROUPS[7],
    22: "4 Αστέρων - Ομάδα %s" % GROUPS[7],
    23: "3 Αστέρων - Ομάδα %s" % GROUPS[7],
    24: "2 Αστέρων - Ομάδα %s" % GROUPS[7],
    25: "1 Αστέρος - Ομάδα %s" % GROUPS[7],

    26: "5 Αστέρων - Ομάδα %s" % GROUPS[8],
    27: "4 Αστέρων - Ομάδα %s" % GROUPS[8],
    28: "3 Αστέρων - Ομάδα %s" % GROUPS[8],
    29: "2 Αστέρων - Ομάδα %s" % GROUPS[8],
    30: "1 Αστέρος - Ομάδα %s" % GROUPS[8],

    31: "5,4,3,2,1 Αστέρων - Ομάδα %s" % GROUPS[9],

    32: "5,4,3,2,1 Αστέρων - Ομάδα %s" % GROUPS[10],

    33: "5,4,3,2,1 Αστέρων - Ομάδα %s" % GROUPS[11],

    34: "Ανεξαρτήτως κατηγορίας - Ομάδα %s" % GROUPS[12],
}

VOTER_MAPPING = {
    (1, '5*****'): 1,
    (1, '4****'): 2,
    (1, '3***'): 3,
    (1, '2**'): 4,
    (1, '1*'): 5,

    (2, '5*****'): 6,
    (2, '4****'): 6,
    (2, '3***'): 6,
    (2, '2**'): 7,
    (2, '1*'): 7,

    (3, '5*****'): 8,
    (3, '4****'): 8,
    (3, '3***'): 8,
    (3, '2**'): 9,
    (3, '1*'): 9,

    (4, '5*****'): 10,
    (4, '4****'): 11,
    (4, '3***'): 12,
    (4, '2**'): 13,
    (4, '1*'): 13,

    (5, '5*****'): 14,
    (5, '4****'): 15,
    (5, '3***'): 16,
    (5, '2**'): 17,
    (5, '1*'): 18,

    (6, '5*****'): 19,
    (6, '4****'): 19,
    (6, '3***'): 19,
    (6, '2**'): 20,
    (6, '1*'): 20, 

    (7, '5*****'): 21,
    (7, '4****'): 22,
    (7, '3***'): 23,
    (7, '2**'): 24,
    (7, '1*'): 25,

    (8, '5*****'): 26,
    (8, '4****'): 27,
    (8, '3***'): 28,
    (8, '2**'): 29,
    (8, '1*'): 30,

    (9, '5*****'): 31,
    (9, '4****'): 31,
    (9, '3***'): 31,
    (9, '2**'): 31,
    (9, '1*'): 31,

    (10, '5*****'): 32,
    (10, '4****'): 32,
    (10, '3***'): 32,
    (10, '2**'): 32,
    (10, '1*'): 32,

    (11, '5*****'): 33,
    (11, '4****'): 33,
    (11, '3***'): 33,
    (11, '2**'): 33,
    (11, '1*'): 33,

    (12, u"Α'ΤΑΞΗΣ"): 34,
    (12, u"Β'ΤΑΞΗΣ"): 34,
    (12, u"Γ'ΤΑΞΗΣ"): 34,
    (12, u"Δ'ΤΑΞΗΣ"): 34,
    (12, u"Ε'ΤΑΞΗΣ"): 34,
}

RATINGS_MAPPING = {
    u"ΠΟΛΥΤΕΛΕΙΑΣ": "5*****",
    u"Α'ΤΑΞΗΣ": "4****",
    u"Β'ΤΑΞΗΣ": "3***",
    u"Γ'ΤΑΞΗΣ": "2**",
    u"Δ'ΤΑΞΗΣ": "1*",
    u"Ε'ΤΑΞΗΣ": "1*",
}

VOTER_BALLOTS = defaultdict(list)

class Command(BaseCommand):
    help = """Extracts voters files"""
        
    def writenl(self, arg):
        self.stdout.write(arg)
        self.stdout.write("\n")

    def extract_voters(self, args, options):
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
            electoral_group_code = establishment.electoral_group.code
            rating = establishment.rating.name
            if electoral_group_code != 12 and rating.find("*") == -1:
                rating = RATINGS_MAPPING[rating]
            key = (electoral_group_code, rating)
            if key not in VOTER_MAPPING:
                raise AssertionError()
                write("{0},{1},{2}".format(key[0], key[1].encode('utf-8'),
                                           establishment))
            else:
                ballot = VOTER_MAPPING[key]
		row.extend(key)
                urow = [c.encode('utf-8') if isinstance(c, basestring) else c
                       for c in row]
                election_name = "Κάλπη %d - " % ballot
                election_name += ELECTION_NAMES[ballot]
                urow.append(election_name)
                VOTER_BALLOTS[ballot].append(urow)
        for ballot in sorted(VOTER_BALLOTS.keys()):
            with open("ballot_{0}.csv".format(ballot), 'wb') as ballot_file:
                ballot_writer = csv.writer(ballot_file)
                for voter in VOTER_BALLOTS[ballot]:
                    ballot_writer.writerow(voter)

    def handle(self, *args, **options):
        self.extract_voters(args, options)



