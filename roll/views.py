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
            voter.name = request.POST.get('voter_name', '')
            voter.email = request.POST.get('voter_email', '')
            voter.mobile_phone = request.POST.get('voter_mobile_phone', '')
            voter.save()
            establishment.voter = voter
            establishment.save()
            return redirect(request.path + '/thanks')
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
