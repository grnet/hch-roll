from django import forms

from django.utils.translation import ugettext_lazy as _

from models import *

from django.core.validators import MinLengthValidator, MaxLengthValidator

def unique_id_exists(unique_id):
    if not Establishment.objects.filter(unique_id=unique_id).exists():
        raise forms.ValidationError(_('unique id does not exist'))

class RegistrationKeyForm(forms.Form):

    unique_id = forms.CharField(
        min_length=19,
        max_length=19,
        label=_('registration unique id'),
        validators=[unique_id_exists])

    def __init__(self, *args, **kwargs):
        super(RegistrationKeyForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.iteritems():
            field.widget.attrs = {
                'class': 'form-control',
            }
    
class RegistrationForm(forms.ModelForm):
    voter_first_name = forms.CharField(max_length=100,
                                       label=_('voter first name'))
    voter_surname = forms.CharField(max_length=100,
                                    label=_('voter surname'))    
    voter_email = forms.EmailField(label=_('voter email'))
    voter_mobile_phone = forms.CharField(max_length=20,
                                         label=_('voter mobile phone'))

    voter_field_names = ('voter_first_name',
                         'voter_surname',
                         'voter_email',
                         'voter_mobile_phone',)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.iteritems():
            field.widget.attrs = {
                'class': 'form-control',
            }
            if not field_name.startswith('voter'):
                field.widget.attrs['readonly'] = 'true'

            if type(field) == forms.ModelChoiceField:
                field.empty_label = None

        if not self.instance:
            return
        self.fields['address'].queryset = Address.objects.filter(
            id=self.instance.address_id)
        self.fields['establishment_type'].queryset = EstablishmentType.objects.filter(id=self.instance.establishment_type_id)
        self.fields['rating'].queryset = Rating.objects.filter(
            id=self.instance.rating_id)
        self.fields['operator'].queryset = Operator.objects.filter(
            id=self.instance.operator_id)
        self.fields['owner'].queryset = Owner.objects.filter(
            id=self.instance.owner_id)
        self.fields['electoral_group'].queryset = ElectoralGroup.objects.filter(
            id=self.instance.electoral_group_id)
    
    def voter_fields(self):
        return [field for field in self.visible_fields()
                if field.name in RegistrationForm.voter_field_names ]

    def non_voter_fields(self):
        return [field for field in self.visible_fields()
                if field.name not in RegistrationForm.voter_field_names ]
            
    class Meta:
        model = Establishment
        exclude = ('license', 'unique_id', 'fee_payment', 'voter',)


