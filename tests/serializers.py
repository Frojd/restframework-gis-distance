# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework_gis_distance.fields import DistanceField
from models import Record


class RecordSerializer(serializers.ModelSerializer):
    distance = DistanceField(unit='m')

    class Meta:
        model = Record
        fields = ('location', 'title', 'created', 'distance')


class RecordOptionalSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Record
        fields = ('location', 'title', 'created', 'distance')

    def get_distance(self, obj):
        distance = getattr(obj, "distance", None)
        return DistanceField(unit='m').to_representation(distance)
