from django.contrib import admin
from apps.auction.models import Auction

class AuctionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Auction,AuctionAdmin)
