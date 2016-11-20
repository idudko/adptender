from django.conf.urls.defaults import patterns

urlpatterns = patterns('apps.auction.views',
    (r'view/(?P<id>\d+)/$', 'view'),
    (r'list/$','list'),
    (r'bet/$','bet_list'),
    (r'dobet/(?P<tender>\d+)/$','do_bet'),
    (r'report/(?P<tender>\d+)/$','get_auction_report'),
)
