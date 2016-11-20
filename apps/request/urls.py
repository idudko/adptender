from django.conf.urls.defaults import patterns

urlpatterns = patterns('apps.request.views',
    (r'^sell/add/$','sell_request_send' ),
    (r'^sell/process/(?P<req_id>\d+)/$','sell_request_process' ),
    (r'^sell/review/(?P<id>\d+)/$','sell_review'),
    (r'^sell/view/(?P<id>\d+)/$','sell_request_view'),
    (r'^sell/list/$','sell_list'),
    (r'^buy/add/(?P<id>\d+)/$','buy_request_add' ),
    (r'^buy/review/(?P<id>\d+)/$','buy_review'),
    (r'^buy/auction/(?P<id>\d+)/$','buy_request_list'),
    (r'^buy/list/$','buy_auction_list'),
    (r'^buy/view/(?P<id>\d+)/$','buy_view'),
    (r'^perm/(?P<type>\d+)/$','is_request_add_permitted'),
    (r'^notification/(?P<req_id>\d+)/$','get_request_notification')
)
