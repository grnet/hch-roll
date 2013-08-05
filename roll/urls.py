from django.conf.urls import patterns, url

from roll import views

urlpatterns = patterns('',
                       url(r'^registration/(?P<unique_id>.+)',
                           views.register,
                           name='register'),
)
