import settings
from django.conf.urls.defaults import *
from apps.profile.forms import CustomRegistrationFormUniqueEmail
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/register/$', 'registration.views.register',
        {'form_class': CustomRegistrationFormUniqueEmail},
        name='registration_register'),
    (r'^accounts/profile/storage', 'apps.storage.views.upload_documents'),
    (r'^accounts/notices/', include('notification.urls')),
    url(r'^accounts/notices/mail/', 'apps.core.views.mail_delivery', name="send_notification"),
    (r'^accounts/profile/edit', 'apps.profile.views.edit'),
    (r'^accounts/profile/', 'apps.profile.views.view'),
    (r'^accounts/buy/(?P<mode>\w+)/', 'apps.profile.views.buy_list'),
    (r'^accounts/sell/auction/(?P<mode>\w+)/', 'apps.profile.views.sell_auction_list'),
    (r'^accounts/sell/stock/(?P<mode>\w+)/', 'apps.profile.views.sell_stock_list'),
    (r'^accounts/', include('registration.urls')),
    (r'^accounts/accreditation/', include('apps.accreditation.urls')),
    (r'^auction/', include('apps.auction.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^defaulter/',include('apps.defaulter.urls')),
    (r'^stock/',include('apps.lot.urls')),
    (r'^accounts/request/',include('apps.request.urls')),
#    (r'^test/', 'apps.storage.views.my_view'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
