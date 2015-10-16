
__author__ = 'LT10'
from django.conf.urls import url, patterns
from . import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^signup/$', views.sign_up, name='signup'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^account/$', views.account_details, name='account'),
                       url(r'^details/(?P<product_id>\w+)$', views.product_details, name='details'),
                       url(r'^products/(?P<category_id>\w+)$', views.products, name='products'),
                       url(r'^cart/$', views.show_cart, name='cart'),




)

