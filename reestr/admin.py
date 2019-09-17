from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import *
from django.contrib import messages
# Register your models here.


class SroStatusFilter(SimpleListFilter):
    title = 'Статус члена СРО'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('a', 'Active'),
            ('na', 'Not Active')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'a':
            # return queryset.distinct().filter(sro_member__status='a')
            return queryset.filter(sro_member__status='a')
        if self.value() == 'na':
            return queryset.filter(sro_member__status='na')


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

def get_sro_member(obj):
    return obj.sro_member


@admin.register(AccreditedCenter)
class AccreditedCenterAdmin(admin.ModelAdmin):

    list_display = ['short_code', get_city, get_sro_member, 'active', 'temporary_suspend_date']
    list_filter = ['short_code', 'active', 'temporary_suspend_date', SroStatusFilter]
    # import pdb; pdb.set_trace()

    def save_model(self, request, obj, form, change):
        if 'active' in form.changed_data:
            if obj.active is True and obj.sro_member.status == 'na':
                messages.add_message(request, messages.WARNING, 'Организация \
                    исключена из реестра СРО, активность центра не может быть \
                        установлена')
        super(AccreditedCenterAdmin, self).save_model(request, obj, form, change)

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