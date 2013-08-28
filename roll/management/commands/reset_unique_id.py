from django.core.management.base import BaseCommand, CommandError

from roll.models import *

import django
from functools import partial

from optparse import make_option
from django.db import transaction

class Command(BaseCommand):
    help = 'Resets unique IDs'
    args = '<unique_id1 unique_id2 ...>'
    option_list = BaseCommand.option_list + (
        make_option('-a',
                    '--all',
                    action='store_true',
                    dest='all',
                    help='Reset all unique IDs',
                    ),
        make_option('-i',
                    '--input',
                    action='store',
                    type='string',
                    dest='input_file',
                    help='file with unique IDs to be reset',
                ),
        )
    
    @transaction.commit_on_success
    def reset_unique_id(self, args, options):
        if django.get_version() >= '1.5':
            write = partial(self.stdout.write, ending = '')
        else:
            write = self.stdout.write
        if options['all']:
            establishments = Establishment.objects.all()
        elif options['input_file']:
            with open(options['input_file'], 'r') as establishments_file:
                unique_ids = [x.rstrip()
                              for x in establishments_file.readlines()]
                establishments = Establishment.objects.filter(
                    unique_id__in=unique_ids)
        else:
            establishments = Establishment.objects.filter(unique_id__in=args)
        for num, establishment in enumerate(establishments):
            establishment.reset_unique_id()
            establishment.save()
            write("\r{0}".format(num+1))
            self.stdout.flush()            
        write("\n")

    def handle(self, *args, **options):
        self.reset_unique_id(args, options)

