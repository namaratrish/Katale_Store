__author__ = 'LT10'
from django.conf.urls import url, patterns
from . import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^signup/$', views.sign_up, name='signup'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^account/$', views.account_details, name='account'),


)
