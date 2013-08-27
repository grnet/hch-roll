from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings

from roll.models import Establishment, Address

from optparse import make_option

import sys
import os
import copy

import django
from functools import partial

from string import Template

import xml.etree.ElementTree as ET

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Arial',
                               os.path.join(settings.FONTS_DIR,
                                            'Arial.ttf')))
pdfmetrics.registerFont(TTFont('Arial Bold',
                               os.path.join(settings.FONTS_DIR,
                                            'Arial Bold.ttf')))
pdfmetrics.registerFont(TTFont('Arial Italic',
                               os.path.join(settings.FONTS_DIR,
                                            'Arial Italic.ttf')))
pdfmetrics.registerFont(TTFont('Arial Bold Italic',
                               os.path.join(settings.FONTS_DIR,
                                            'Arial Bold Italic.ttf')))

from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily('Arial',
                   normal='Arial',
                   bold='Arial Bold',
                   italic='Arial Italic',
                   boldItalic='Arial Bold Italic')

WINDOW_ORIGIN_X = 7*cm
WINDOW_ORIGIN_Y = 3*cm

class Command(BaseCommand):
    help = """Creates voter notifications. If no recipients file is given,
recipients are taken from the command line, unless the -a option is
passed, in which case notifications are created for all voters
currently in the the database, or the -i option is passed, in which
case notifications are created for the recipients contained in the
input file. Recipients are indicated by their unique IDs"""
    args = '<unique_id1 unique_id2 ...>'
    option_list = BaseCommand.option_list + (
        make_option('-a',
                    '--all',
                    action='store_true',
                    dest='all',
                    help='Create notifications for all establishments',
                ),
        make_option('-i',
                    '--input',
                    action='store',
                    type='string',
                    dest='input_file',
                    help='set recipients file',
                    ),
        make_option('-t',
                    '--template',
                    action='store',
                    type='string',
                    dest='template_file',
                    help='template file for document content',
                ),
        make_option('-d',
                    '--destination_dir',
                    action='store',
                    type='string',
                    dest='destination_dir',
                    help='destination directory for PDF file',
                ),
        make_option('-f',
                    '--filename',
                    action='store',
                    type='string',
                    dest='destination_filename',
                    default='output.pdf',
                    help='PDF file name',
                ),        
    )

    def layout_notice(self, establishment, notice_template, mapping,
                      notices, window_style, style):
        notices.append(Spacer(0, WINDOW_ORIGIN_Y))
        address_window_text = '\n'.join([
            establishment.establishment_type.name,
            u"{0} ({1})".format(establishment.name,
                                establishment.registry_number),
            establishment.owner.name,
            establishment.address.street_number,
            establishment.address.zip_code,
            establishment.address.city.name])       
        address_window = Preformatted(address_window_text, window_style)
        notices.append(address_window)
        notices.append(Spacer(0, 2*cm))
        if notice_template is not None:
            notice = notice_template.safe_substitute(mapping)
            xmldoc = ET.fromstring(notice)
            for para in xmldoc.findall('para'):
                para_str = ET.tostring(para, encoding="utf-8")
                notices.append(Paragraph(para_str, style))
        notices.append(PageBreak())
        return notices
        
    def make_notices(self, args, options):
        if django.get_version() >= '1.5':
            write = partial(self.stdout.write, ending = '')
        else:
            write = self.stdout.write
        if options['template_file']:
            template_file = open(options['template_file'], 'r')
            template_contents = template_file.read()
            notice_template = Template(template_contents)
        else:
            notice_template = Template("")
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

        notices = []
        styles = getSampleStyleSheet()
        body_style = styles['Normal']
        body_style.fontName = 'Arial'
        body_style.fontSize = 10
        body_style.spaceAfter = 10
        window_style = copy.copy(body_style)
        window_style.leftIndent = WINDOW_ORIGIN_X
        if options['destination_dir']:
            destination = os.path.join(options['destination_dir'],
                                       options['destination_filename'])
        else:
            destination = options['destination_filename']
        for num_establishment, establishment in enumerate(establishments):
            mapping = {
                'unique_id': establishment.unique_id.encode('utf-8'),
            }
            notices = self.layout_notice(establishment,
                                         notice_template,
                                         mapping,
                                         notices,
                                         window_style,
                                         body_style)
            write("\r{0}".format(num_establishment+1))
            self.stdout.flush()
        doc = SimpleDocTemplate(destination, pagesize=A4)
        doc.build(notices)
        self.stdout.write("")        

    def handle(self, *args, **options):
        self.make_notices(args, options)



