from django.contrib import admin
from apps.defaulter.models import Defaulter

class DefaulterAdmin(admin.ModelAdmin):
    pass

admin.site.register(Defaulter,DefaulterAdmin)