from django import forms

from models import * 

class RegistrationForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):        
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.iteritems():
            field.widget.attrs = {
                'class': 'form-control',
                'readonly': 'readonly'
            }        
        self.fields['location'].queryset = Location.objects.filter(
            id=self.instance.location_id)
        self.fields['rating'].queryset = Rating.objects.filter(
            id=self.instance.rating_id)
        self.fields['operator'].queryset = Operator.objects.filter(
            id=self.instance.operator_id)
        self.fields['owner'].queryset = Owner.objects.filter(
            id=self.instance.owner_id)
        self.fields['electoral_group'].queryset = ElectoralGroup.objects.filter(
            id=self.instance.electoral_group_id)        

    class Meta:
        model = Establishment
        exclude = ('license', 'unique_id', 'fee_payment',)

