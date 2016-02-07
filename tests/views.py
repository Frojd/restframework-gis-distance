# -*- coding: utf-8 -*-

from django.http import (
    Http404
)
from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny
from rest_framework_gis_distance.filters import OrderedDistanceToPointFilter
from models import Record
from serializers import (
    RecordOptionalSerializer, RecordSerializer
)


class RecordListView(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RecordSerializer
    queryset = Record.objects.all()
    filter_backends = (OrderedDistanceToPointFilter,)
    distance_filter_field = 'location'
    distance_filter_convert_meters = True
    distance_filter_add_distance = True

    def get(self, request, *args, **kwargs):
        if not self.request.query_params.get('point', None):
            raise Http404()

        return self.list(request, *args, **kwargs)


class RecordOptionalListView(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RecordOptionalSerializer
    queryset = Record.objects.all()
    filter_backends = (OrderedDistanceToPointFilter,)
    distance_filter_field = 'location'
    distance_filter_convert_meters = True
    distance_filter_add_distance = True

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
