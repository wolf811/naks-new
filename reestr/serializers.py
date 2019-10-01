from rest_framework import serializers


from .models import AccreditedCenter, Level, WeldType, GTU, Activity


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ('level',)


class WeldTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeldType
        fields = ('short_name', 'full_name')


class GTUSerializer(serializers.ModelSerializer):
    class Meta:
        model = GTU
        fields = ('short_name', 'full_name', 'parent')


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('short_name', 'full_name')


class DirectoriesSerializer(serializers.Serializer):
    levels = serializers.SerializerMethodField()
    weldtypes = serializers.SerializerMethodField()
    gtus = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()

    class Meta:
        # model = Level
        fields = (
            'levels',
            'weldtypes',
            'gtus',
            'activities',
        )

    def get_weldtypes(self, obj):
        weldtypes = WeldType.objects.all()
        serialized_weldtypes = WeldTypesSerializer(weldtypes, many=True)
        return serialized_weldtypes.data

    def get_levels(self, obj):
        levels = Level.objects.all()
        serialized_levels = LevelSerializer(levels, many=True)
        return serialized_levels.data

    def get_gtus(self, obj):
        gtus = GTU.objects.all()
        serialized_gtus = GTUSerializer(gtus, many=True)
        return serialized_gtus.data

    def get_activities(self, obj):
        activities = Activity.objects.all()
        serialized_activities = ActivitySerializer(activities, many=True)
        return serialized_activities.data


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
            'activities',
            'sm_types',
            'so_types',
            'profstandards',
            'profqualifications',
        )

    def get_city(self, obj):
        return obj.sro_member.city.title
