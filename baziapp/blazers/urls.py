from django.conf.urls import patterns, include, url
from blazers import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blazers.views.home', name='home'),
    # url(r'^blazers/', include('blazers.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    #url(r'^hello/$',views.hello),
    url(r'^$',views.post),
    url(r'^query/$',views.query),
    url(r'^qrquery/$',views.qrquery),
    url(r'^contact/$',views.contact),
    url(r'^about/$',views.about),
    url(r'^bazi/$',views.post),
)
