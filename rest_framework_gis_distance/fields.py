from django.contrib.gis.measure import Distance
from rest_framework import serializers


class DistanceField(serializers.BaseSerializer):
    def __init__(self, unit='m', **kwargs):
        super(DistanceField, self).__init__(**kwargs)
        if unit not in Distance.UNITS:
            raise Exception(
                "Unit '%s' not allowed. Unit must be a django supported unit" %
                unit)

        self.unit = unit

    def to_representation(self, value):
        if not isinstance(value, Distance):
            return -1

        return getattr(value, self.unit)
