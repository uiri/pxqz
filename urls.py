from django.conf.urls import patterns, include, url
import pastadish.views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       ('^clear$', pastadish.views.clean),
                       ('^[0-9a-fA-F]+/edit$', pastadish.views.edit),
                       ('^[0-9a-fA-F]+/html$', pastadish.views.html),
                       ('^.+$', pastadish.views.retrieve),
                       ('^$', pastadish.views.index),
    # Examples:
    # url(r'^$', 'pxqz.views.home', name='home'),
    # url(r'^pxqz/', include('pxqz.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
