from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

app_patterns = patterns('',
    # Examples:
    # url(r'^$', 'hch-roll.views.home', name='home'),
    # url(r'^hch-roll/', include('elections.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^roll/', include('roll.urls')),
)

urlpatterns = patterns('', url('^r/', include(app_patterns)))
