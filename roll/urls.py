from django.conf.urls import patterns, url

from roll import views

urlpatterns = patterns('',
                       url(r'^registration/(?P<establishment_id>\d+)/thanks',
                           views.register_thanks,
                           name='register_thanks'),                       
                       url(r'^registration/(?P<establishment_id>\d+)',
                           views.register,
                           name='register'),
)
