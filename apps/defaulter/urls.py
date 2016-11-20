# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns

urlpatterns = patterns('apps.defaulter.views',
    (r'^view/(?P<id>\d+)/$','view'),
    (r'^list/$','list'),
)
