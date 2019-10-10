from rest_framework import serializers
from .useful import serializer_factory


from .models import AccreditedCenter, Level, WeldType, GTU, Activity
from .models import SM, SO, PS, PK


def create_serializer_class(cls, fields=None):
    Meta = type('Meta', (type,), {'model': cls, 'fields': fields})
    new_cls = type(cls.__name__+'Serializer', (serializers.ModelSerializer,), {
        'Meta': Meta,
    })
    return new_cls


class LevelSerializer(serializers.ModelSerializer):
    # import pdb; pdb.set_trace()
    class Meta:
        model = Level
        fields = ('id', 'level',)
# import pdb; pdb.set_trace()


class WeldTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeldType
        fields = ('id', 'short_name', 'full_name')


class GTUSerializer(serializers.ModelSerializer):
    class Meta:
        model = GTU
        fields = ('id', 'short_name', 'full_name', 'parent')


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'short_name', 'full_name')


class DirectoriesSerializer(serializers.Serializer):
    levels = serializers.SerializerMethodField()
    weldtypes = serializers.SerializerMethodField()
    gtus = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()
    sm = serializers.SerializerMethodField()
    so = serializers.SerializerMethodField()

    class Meta:
        # model = Level
        fields = (
            'levels',
            'weldtypes',
            'gtus',
            'activities',
            'sm',
            'so',
        )

    def get_so(self, obj):
        all_so_types = SO.objects.all()
        so_serializer = create_serializer_class(SO, ('id', 'short_name', 'full_name', 'parent'))
        serialized_so = so_serializer(all_so_types, many=True)
        return serialized_so.data

    def get_sm(self, obj):
        all_sm_types = SM.objects.all()
        sm_serializer = serializer_factory(SM, ['id', 'short_name', 'full_name', 'parent'])
        serialized_sm = sm_serializer(all_sm_types, many=True)
        return serialized_sm.data

    def get_weldtypes(self, obj):
        weldtypes = WeldType.objects.all()
        serialized_weldtypes = WeldTypesSerializer(weldtypes, many=True)
        # import pdb; pdb.set_trace()
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
        try:
            return obj.sro_member.city.title
        except Exception as e:
            print('CITY ERROR', obj, e)
            return ''
