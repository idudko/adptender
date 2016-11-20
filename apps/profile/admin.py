from django.contrib import admin
from apps.profile.models import Country,Profile, Region, PopulatedLocalityType

class CountryAdmin(admin.ModelAdmin):
    list_per_page = 25
    search_fields = ('name',)

class RegionAdmin(admin.ModelAdmin):
    list_per_page = 25
    search_fields = ('name',)

class PopulatedLocalityTypeAdmin(admin.ModelAdmin):
    list_per_page = 25
    search_fields = ('name',)

admin.site.register(Country,CountryAdmin)
admin.site.register(Region,RegionAdmin)
admin.site.register(PopulatedLocalityType,PopulatedLocalityTypeAdmin)
admin.site.register(Profile)
