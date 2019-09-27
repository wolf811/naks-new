from rest_framework import serializers


from .models import AccreditedCenter, Level, WeldType, GTU, Activity


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level


class WeldTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeldType


class GTUSerializer(serializers.ModelSerializer):
    class Meta:
        model = GTU


class ActivitySerialize(serializers.ModelSerializer):
    class Meta:
        model = Activity


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
            'special_tn',
            'special_gp',
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
