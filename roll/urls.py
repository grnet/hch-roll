from django.conf.urls import patterns, url

from roll import views

urlpatterns = patterns('',
                       url(r'^registration/(?P<unique_id>.+)/thanks',
                           views.register_thanks,
                           name='register_thanks'),                       
                       url(r'^registration/(?P<unique_id>.+)',
                           views.register,
                           name='register'),
)
