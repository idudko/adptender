# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns

urlpatterns = patterns('apps.lot.views',
    (r'^view/(?P<id>\d+)/$','view'),
    (r'^list/defaulter/(?P<defaulter_id>\d+)/$','list'),
)