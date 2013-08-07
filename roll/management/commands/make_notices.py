from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings

from roll.models import Establishment, Address

from optparse import make_option

import sys
import os

from string import Template

import xml.etree.ElementTree as ET

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Linux Libertine',
                               os.path.join(settings.FONTS_DIR,
                                            'LinLibertine_Rah.ttf')))

PAGE_WIDTH, PAGE_HEIGHT = A4
ENVELOPE_WIDTH = 23*cm
ENVELOPE_HEIGHT = 11.5*cm
ENVELOPE_MARGIN_X = 2*cm
ENVELOPE_MARGIN_Y = 2*cm
WINDOW_WIDTH = 10.5*cm
WINDOW_HEIGHT = 4.5*cm
WINDOW_ORIGIN_X = PAGE_WIDTH - WINDOW_WIDTH - ENVELOPE_MARGIN_X
WINDOW_ORIGIN_Y = PAGE_HEIGHT - ENVELOPE_HEIGHT + ENVELOPE_MARGIN_Y
BODY_MARGIN = 2.5*cm
BODY_ORIGIN_X = BODY_MARGIN
BODY_ORIGIN_Y = BODY_MARGIN
BODY_HEIGHT = PAGE_HEIGHT - ENVELOPE_HEIGHT - ENVELOPE_MARGIN_Y
BODY_WIDTH = PAGE_WIDTH - 2 * BODY_MARGIN

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
                    help='Create notifications for all participants',
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
    )

    def make_notice(self, participant, mapping, notice_template):
        mapping.update({
            'unique_id': participant.unique_id.encode('utf-8'),
            })
        body = []
        if notice_template is not None:
            notice = notice_template.safe_substitute(mapping)
            xmldoc = ET.fromstring(notice)
            styles = getSampleStyleSheet()
            styleN = styles['Normal']
            styleN.fontName = 'Linux Libertine'
            for para in xmldoc.iter('para'):
                para_str = ET.tostring(para, encoding="utf-8", method="xml")
                body.append(Paragraph(para_str, styleN))
        c = canvas.Canvas(participant.unique_id + ".pdf", pagesize=A4)
        doc = SimpleDocTemplate(participant.unique_id + ".pdf", pagesize=A4)
        c.rect(WINDOW_ORIGIN_X, WINDOW_ORIGIN_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
        address_window = c.beginText()
        c.setFont('Linux Libertine', 12)        
        address_window.setFont('Linux Libertine', 12)
        address_window.setTextOrigin(WINDOW_ORIGIN_X + 0.5*cm,
                                     WINDOW_ORIGIN_Y + WINDOW_HEIGHT - 0.5*cm)
        address_window.textLine(participant.name)
        address_window.textLine(participant.address.street_number)
        address_window.textLine(participant.address.zip_code)
        address_window.textLine(str(participant.address.city))
        c.drawText(address_window)
        f = Frame(BODY_ORIGIN_X, BODY_ORIGIN_Y, BODY_WIDTH, BODY_HEIGHT,
                  showBoundary=0)
        f.addFromList(body, c)
        return c
                
    def make_notices(self, args, options):
        if options['template_file']:
            template_file = open(options['template_file'], 'r')
            template_contents = template_file.read()
            notice_template = Template(template_contents)
        else:
            notice_template = Template("")
        if options['all']:
            participants = Establishment.objects.all()
        elif options['input_file']:
            with open(options['input_file'], 'r') as participants_file:
                emails = [x.rstrip() for x in participants_file.readlines()]
                participants = Establishment.objects.filter(
                    voter__email__in=emails)
        else:
            participants = Establishment.objects.filter(unique_id__in=args)
        
        for participant in participants:
            notice = self.make_notice(participant,
                                      {},
                                      notice_template)
            notice.save()
            
    def handle(self, *args, **options):
        self.make_notices(args, options)
        
        
        
