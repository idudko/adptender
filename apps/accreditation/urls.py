from django.conf.urls.defaults import patterns

urlpatterns = patterns('apps.accreditation.views',
    (r'list/$','list'),
    (r'add/$', 'add'),
    (r'review/(?P<id>\d+)/$', 'review'),
    (r'view/(?P<id>\d+)/$', 'view'),
)
