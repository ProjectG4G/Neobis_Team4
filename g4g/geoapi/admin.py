from django.contrib import admin

from .models import Country, Region, District, Village


# Register your models here.

class VillageAdmin(admin.ModelAdmin):
    search_fields = ['name__icontains']
    list_display = ('name', 'get_district_name', 'get_city_name', 'get_region_name')

    list_filter = ('district__region', 'district',)

    @admin.display(description="Район", ordering="district__region_name")
    def get_district_name(self, obj):
        if obj.district and obj.district.type == 1:
            return obj.district.name
        else:
            return "жок"

    @admin.display(description="Шаар", ordering="district__region__name")
    def get_city_name(self, obj):
        if obj.district and obj.district.type == 2:
            return obj.district.name
        else:
            return "жок"

    @admin.display(description="Облус", ordering="region__name")
    def get_region_name(self, obj):
        return obj.district.region.name


admin.site.register(Country)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(Village, VillageAdmin)
