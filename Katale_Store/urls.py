"""Katale_Store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.conf.urls import url, patterns
from Katale_Store import settings
from Katale import urls as Katale_urls


urlpatterns = [
    url(r'^Katale/', include(Katale_urls, namespace='Katale')),
    url(r'^admin/', include(admin.site.urls)),

]

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static', (r'media/(?P<path>.*)',
                                'serve',
                                {'document_root': settings.MEDIA_ROOT})
    )

# THE IF LETS US CHECK IF THE PROJECT IS BEING RUN IN DEBUG MODE,I.E DEBUG IS TRUE

# THE NEW PATTERN
# ADDED MINS IF ANY FILE IS REQUESTED
# WITH A URL STATING WITH MEDIA/ THE REQUEST
# WILL B PASD TO THE DJANGO.VIEWS.STATIC VIEW
