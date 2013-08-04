from django.forms import ModelForm

from models import Establishment

class RegistrationForm(ModelForm):

    class Meta:
        model = Establishment

