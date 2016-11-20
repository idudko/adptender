from django.contrib import admin
from apps.auction.models import SellRequest

class RequestAdmin(admin.ModelAdmin):
    pass

admin.site.register(SellRequest,RequestAdmin)
