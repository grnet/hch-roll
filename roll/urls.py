from django.conf.urls import patterns, url

from roll import views

urlpatterns = patterns('',
                       url(r'^registration-closed',
                           views.registration_closed,
                           name='registration_closed'),                       
                       url(r'^registration/(?P<unique_id>.+)',
                           views.register,
                           name='register'),
                       url(r'^registration',
                           views.register_key,
                           name='register_key'),
)
