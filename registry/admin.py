from django.contrib import admin
from django.forms import ModelForm
from django.contrib.postgres.fields import JSONField
from prettyjson import PrettyJSONWidget
from .models import *
from rangefilter.filter import DateRangeFilter

# Register your models here.
import json
import logging

# logger = logging.getLogger(__name__)

# class PrettyJSONWidget(widgets.Textarea):
#     # import pdb; pdb.set_trace()
#     def format_value(self, value):
#         try:
#             value = json.loads(value)
#             # value = json.dumps(json.loads(value), indent=2, sort_keys=True)
#             # these lines will tpry to adjust size of TextArea to fit to content
#             row_lengths = [len(r) for r in value.split('\n')]
#             self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
#             self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
#             return value
#         except Exception as e:
#             logger.warning("Error while formatting JSON: {}".format(e))
#             return super(PrettyJSONWidget, self).format_value(value)
# admin.site.register(RegistryRecordPersonal)
# class JsonForm(ModelForm):
#   class Meta:
#     model = RegistryRecordPersonal
#     fields = '__all__'
#     widgets = {
#       'data': PrettyJSONWidget(),
#     }


@admin.register(RegistryRecordPersonal)
class RegistryRecordPersonalAdmin(admin.ModelAdmin):
    # form = JsonForm
    list_display = ('id', 'fio', 'udost_number', 'obl_att', 'place_of_att', 'date_created')
    list_display_links = ('id', 'fio')
    fields = ('fio', 'data', 'company', 'date_created', 'active_since', 'active_until', 'extension_date', 'edo_id')
    list_filter = (('date_created', DateRangeFilter),)
    search_fields = ['fio', 'data']
    readonly_fields = ('company', 'edo_id')

    formfield_overrides = {
        JSONField : {'widget': PrettyJSONWidget(attrs={'initial': 'parsed'}) }
    }

    def obl_att(self, instance):
        try:
            activity = instance.data['activity']
            gtus = instance.data['gtus']
            return '{}-{}'.format(activity, gtus)
        except Exception as e:
            return 'ошибка обл. атт.: {}'.format(e)

    def udost_number(self, instance):
        try:
            udost_number = instance.data['udost']
            return '{}'.format(udost_number)
        except Exception as e:
            return 'ошибка номера: {}'.format(e)

    def place_of_att(self, instance):
        try:
            place_of_att = instance.data['place_of_att']
            return place_of_att
        except Exception:
            return '-'

admin.site.register(Company)