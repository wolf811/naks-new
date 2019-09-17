from django.contrib import admin
from .models import *
# Register your models here.

def get_accred_centers(obj):
    return ", ".join(
        [center.short_code for center in AccreditedCenter.objects.filter(sro_member=obj)])


def get_city(obj):
    return obj.sro_member.city

class AccreditedCenterInline(admin.StackedInline):
    model = AccreditedCenter
    extra = 0


@admin.register(SROMember)
class SROMemberAdmin(admin.ModelAdmin):
    list_display = ['short_name', 'status', get_accred_centers]
    inlines = [AccreditedCenterInline]

@admin.register(AccreditedCenter)
class AccreditedCenterAdmin(admin.ModelAdmin):
    list_display = ['short_code', get_city, 'active', 'temporary_suspend_date']

admin.site.register(Level)
admin.site.register(PS)
admin.site.register(PK)
admin.site.register(SM)
admin.site.register(SO)
admin.site.register(GTU)
admin.site.register(WeldType)
# admin.site.register(SROMember)
# admin.site.register(AccreditedCenter)
admin.site.register(CheckProtocol)
admin.site.register(City)