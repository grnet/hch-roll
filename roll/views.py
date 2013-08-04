from django.shortcuts import render, redirect

from django.http import HttpResponse

from models import Establishment

from forms import RegistrationForm

def register(request, unique_id=None):
    establishment = None
    if unique_id:
        establishment = Establishment.objects.get(unique_id=unique_id)
    if request.method == 'POST':
        if establishment_id:
            form = RegistrationForm(request.POST, instance=establishment)
        else:
            form = RegistrationForm(request.POST)
        if form.is_valid():
            establishment = form.save()
            return redirect('/roll/registration-thanks')
    else:
        if unique_id:
            form = RegistrationForm(instance=establishment)
        else:
            form = RegistrationForm()
    return render(request, 'roll/registration.html', {
        'form': form,
    })

def register_thanks(request, establishment_id=None):
        return render(request, 'roll/thanks.html')
