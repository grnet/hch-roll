from django import forms

from models import * 

class RegistrationForm(forms.ModelForm):
    voter_name = forms.CharField(max_length=200)
    voter_email = forms.EmailField()
    voter_mobile_phone = forms.CharField(max_length=20)

    voter_field_names = ('voter_name', 'voter_email', 'voter_mobile_phone',)

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

    
