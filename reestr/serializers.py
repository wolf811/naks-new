from rest_framework import serializers


from .models import AccreditedCenter


class CenterSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()

    class Meta:
        model = AccreditedCenter
        fields = (
            'id',
            'city',
            'active',
            'active_since',
            'active_until',
            'temporary_suspend_date',
            'chief',
            'sro_member',
            'direction',
            'special',
            'short_code',
            'weldtypes',
            'gtus',
            'levels',
            'acitvities',
            'sm_types',
            'so_types',
            'profstandards',
            'profqualifications',
        )

    def get_city(self, obj):
        return obj.sro_member.city.title
