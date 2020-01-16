from rest_framework import serializers
from .useful import serializer_factory


from .models import AccreditedCenter, Level, WeldType, GTU, Activity, AccreditedCertificationPoint
from .models import SM, SO, Qualification, SROMember


def create_serializer_class(cls, fields=None):
    Meta = type('Meta', (type,), {'model': cls, 'fields': fields})
    new_cls = type(cls.__name__+'Serializer', (serializers.ModelSerializer,), {
        'Meta': Meta,
    })
    return new_cls


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ('id', 'level',)


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
    qualifications = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'levels',
            'weldtypes',
            'gtus',
            'activities',
            'sm',
            'so',
            'qualifications'
        )


    def get_qualifications(self, obj):
        all_qualifications = Qualification.objects.all()
        qualification_serializer = create_serializer_class(Qualification, ('id', 'short_name', 'full_name', 'parent'))
        serialized_qualifications = qualification_serializer(all_qualifications, many=True)
        return serialized_qualifications.data

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
    company = serializers.SerializerMethodField()
    active_since = serializers.DateField(format='%d.%m.%Y')
    active_until = serializers.DateField(format='%d.%m.%Y')
    actual_address = serializers.SerializerMethodField()
    coordinates = serializers.SerializerMethodField()
    company_full_name = serializers.SerializerMethodField()
    cert_points = serializers.SerializerMethodField()

    class Meta:
        model = AccreditedCenter
        fields = (
            'id',
            'city',
            'company',
            'company_full_name',
            'active',
            'actual_address',
            'coordinates',
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
            'qualifications',
            'cok_nark_code',
            'cert_points',
        )

    def get_cert_points(self, obj):
        try:
            points = [p.id for p in AccreditedCertificationPoint.objects.filter(parent=obj)]
            return points
        except Exception as e:
            print('CERT POINTS ERORR', e)
            return []

    def get_company_full_name(self, obj):
        try:
            return obj.sro_member.full_name
        except Exception as e:
            print('COMPANY ERROR', e)
            return 'company_name'

    def get_actual_address(self, obj):
        try:
            return obj.sro_member.actual_address
        except Exception as e:
            print('ADDRESS ERROR', e)
            return 'full_address'

    def get_coordinates(self, obj):
        try:
            return map(lambda x: float(x), obj.sro_member.coordinates.split(" "))
        except Exception as e:
            print('COORDINATES ERROR', e)
            return []

    def get_company(self, obj):
        try:
            return obj.sro_member.short_name
        except Exception as e:
            print('TITLE ERROR', obj, e)
            return ''

    def get_city(self, obj):
        try:
            return obj.sro_member.city.title
        except Exception as e:
            print('CITY ERROR', obj, e)
            return ''


class SROMemberSerializer(serializers.ModelSerializer):
    centers = serializers.SerializerMethodField()
    coordinates = serializers.SerializerMethodField()
    class Meta:
        model = SROMember
        fields = (
            'id',
            'short_name',
            'full_name',
            'actual_address',
            'phone',
            'email',
            'svid_number',
            'centers',
            'coordinates'
            )

    def get_coordinates(self, obj):
        if obj.coordinates:
            return obj.coordinates.split(" ")
        return ['no coordinates']

    def get_centers(self, obj):
        return " ".join([c.short_code for c in AccreditedCenter.objects.filter(active=True, sro_member=obj)])