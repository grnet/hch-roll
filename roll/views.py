from django.shortcuts import render, redirect

from django.http import HttpResponse

from models import Establishment, Voter

from forms import RegistrationForm

def register(request, unique_id=None):
    establishment = None
    voter = None
    if unique_id:
        establishment = Establishment.objects.get(unique_id=unique_id)
        if establishment.voter_id:
            voter = establishment.voter
        else:
            voter = Voter()
    if request.method == 'POST':
        if unique_id:
            form = RegistrationForm(request.POST, instance=establishment)
        else:
            form = RegistrationForm(request.POST)
        if form.is_valid():
            voter.name = form.cleaned_data['voter_name']
            voter.email = form.cleaned_data['voter_email']
            voter.mobile_phone = form.cleaned_data['voter_mobile_phone']
            voter.save()

            # is_valid changes the instance. Invalidate, in order to avoid
            # storing those changes.
            establishment = Establishment.objects.get(unique_id=unique_id)
            establishment.voter = voter
            establishment.save()
            return render(request, 'roll/thanks.html', {
                'voter_name': voter.name,
                'voter_email': voter.email,
                'voter_mobile_phone': voter.mobile_phone,
                'registration_url': request.path
            })
    else:
        if unique_id:
            form = RegistrationForm(
                instance=establishment,
                initial={
                    'voter_name': voter.name,
                    'voter_email': voter.email,
                    'voter_mobile_phone': voter.mobile_phone,
                })
        else:
            form = RegistrationForm()
    return render(request, 'roll/registration.html', {
        'form': form,
        'voter': voter,
        'form_action': request.path,
    })

def register_thanks(request, unique_id=None):
        return render(request, 'roll/thanks.html')
