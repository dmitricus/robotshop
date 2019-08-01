from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView
import mainapp.views as mainapp


urlpatterns = [
    url(r'^$', mainapp.catalog, name='index'),
    url(r'^category/(?P<pk>\d+)/$', mainapp.catalog, name='category'),
    url(r'^product/(\d+)/$', mainapp.product, name='product'),
    url(r'^category/(?P<pk>\d+)/page/(?P<page>\d+)/$', mainapp.catalog, name='page'),

]