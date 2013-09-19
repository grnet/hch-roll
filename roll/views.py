from django.shortcuts import render, redirect, get_object_or_404

from models import Establishment, Voter

from forms import *

from functools import wraps

from django.conf import settings

from datetime import datetime

REGISTRATION_END = None
if hasattr(settings, 'REGISTRATION_END'):
    REGISTRATION_END = datetime.strptime(settings.REGISTRATION_END,
                                         "%Y-%m-%dT%H:%M:%S")
def registration_active(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if REGISTRATION_END is not None and datetime.now() > REGISTRATION_END:
            return redirect('registration_closed')
        else:
            return f(request, *args, **kwargs)
    return wrapper

@registration_active
def register_key(request):
    request.session['django_language'] = 'el'
    if request.method == 'POST':
        form = RegistrationKeyForm(request.POST)
        if form.is_valid():
            unique_id = form.cleaned_data['unique_id']
            return redirect('register', unique_id=unique_id)
    else:
        form = RegistrationKeyForm()
    return render(request, 'roll/registration-key.html', {
        'form': form,
    })

@registration_active
def register(request, unique_id=None):
    request.session['django_language'] = 'el'
    establishment = None
    voter = None
    if unique_id:
        establishment = get_object_or_404(Establishment,
                                          unique_id=unique_id)
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
            voter.first_name = form.cleaned_data['voter_first_name']
            voter.surname = form.cleaned_data['voter_surname']
            voter.email = form.cleaned_data['voter_email']
            voter.mobile_phone = form.cleaned_data['voter_mobile_phone']
            voter.save()

            # is_valid changes the instance. Invalidate, in order to avoid
            # storing those changes.
            establishment = Establishment.objects.get(unique_id=unique_id)
            establishment.voter = voter
            establishment.save()
            return render(request, 'roll/thanks.html', {
                'voter_first_name': voter.first_name,
                'voter_surname': voter.surname,
                'voter_email': voter.email,
                'voter_mobile_phone': voter.mobile_phone,
                'registration_url': request.path
            })
    else:
        if unique_id:
            form = RegistrationForm(
                instance=establishment,
                initial={
                    'voter_first_name': voter.first_name,
                    'voter_surname': voter.surname,
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

@registration_active
def register_thanks(request, unique_id=None):
    return render(request, 'roll/thanks.html')
        
def registration_closed(request):
    return render(request, 'roll/registration_closed.html', {
        'registration_end': REGISTRATION_END,
    })
