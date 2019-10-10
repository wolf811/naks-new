from collections import OrderedDict
from rest_framework.serializers import ModelSerializer

DIRECTIONS = {
        "personal": {
            "title": "personal",
            "registry_name": "Реестр центров, осуществляющих аттестацию сварщиков \
            и специалистов сварочного производства",
            "centers_plural": "Аттестационные центры персонала"
        },
        "specpod": {
            "title": "specpod",
            "registry_name": "Реестр центров специальной подготовки",
            "centers_plural": "Центры специальной подготовки"
        },
        "attsm": {
            "title": "attsm",
            "registry_name": "Реестр центров, осуществляющих аттестацию \
                сварочных материалов",
            "centers_plural": "Аттестационные центры сварочных материалов"
        },
        "attso": {
            "title": "attso",
            "registry_name": "Реестр центров, осуществляющих аттестацию \
                сварочного оборудования",
            "centers_plural": "Аттестационные центры сварочного оборудования"
        },
        "attst": {
            "title": "attst",
            "registry_name": "Реестр центров, осуществляющих \
                аттестацию сварочных технологий",
            "centers_plural": "Аттестационные центры сварочных технологий"
        },
        "qualification": {
            "title": "qualification",
            "registry_name": "Реестр центров оценки квалификации в области сварки \
            и контроля",
            "centers_plural": "Центры оценки квалификации в области сварки и \
                контроля"
        },
        "certification": {
            "title": "qualification",
            "registry_name": "Реестр центров добровольной сертификации \
            в области сварки",
            "centers_plural": "Центры добровольной сертификации"
        }
    }


def serializer_factory(mdl, fields=None, **kwargs):
    """ Generalized serializer factory to increase DRYness of code.

    :param mdl: The model class that should be instanciated
    :param fields: the fields that should be exclusively present on the serializer
    :param kwargs: optional additional field specifications
    :return: An awesome serializer
    """

    def _get_declared_fields(attrs):
        fields = [(field_name, attrs.pop(field_name))
                  for field_name, obj in list(attrs.items())
                  if isinstance(obj, Field)]
        fields.sort(key=lambda x: x[1]._creation_counter)
        return OrderedDict(fields)

    # Create an object that will look like a base serializer
    class Base(object):
        pass

    Base._declared_fields = _get_declared_fields(kwargs)

    class MySerializer(Base, ModelSerializer):
        class Meta:
            model = mdl

        if fields:
            setattr(Meta, "fields", fields)

    return MySerializer


# SPR_SET_FOR_DIRECTION = {
#         "personal": [],
#         "attsm": {

#         },
#         "attso": {

#         },
#         "attst": {

#         },
#         "qualification": {

#         }
#     }