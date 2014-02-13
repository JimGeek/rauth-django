from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'sociallogin.views.home', name='home'),
    url(r'^logintwitter/', 'sociallogin.views.LoginTwitter', name='logintwitter'),
    url(r'^loginfacebook/', 'sociallogin.views.LoginFacebook', name='loginfacebook'),
	url(r'^logingoogle/', 'sociallogin.views.LoginGoogle', name='logingoogle'),

    # url(r'^rauthtest/', include('rauthtest.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
