from django.contrib import admin
from apps.lot.models import Lot

class LotAdmin(admin.ModelAdmin):
    pass

admin.site.register(Lot,LotAdmin)
