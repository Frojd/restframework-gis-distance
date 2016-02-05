# -*- coding: utf-8 -*-

"""
This is an extension to django-restframework-gis that extends on
DistanceToPointFilter and adds sorting by distance.

It is also possible to add a extra distance field to the returned queryset by
adding the flag distance_filter_add_distance = True to the DRF View.
"""

from django.contrib.gis.db.models.functions import Distance
from rest_framework_gis.filters import DistanceToPointFilter


class OrderedDistanceToPointFilter(DistanceToPointFilter):
    def filter_queryset(self, request, queryset, view):
        """
        Add sorting by distance, in addition to DinstanceToPointerFilter filter
        """
        filter_field = getattr(view, 'distance_filter_field', None)
        distance_srid = getattr(view, 'distance_srid', 4326)
        point = self.get_filter_point(request)

        queryset = super(OrderedDistanceToPointFilter, self)\
            .filter_queryset(request, queryset, view)

        if not filter_field:
            return queryset

        if not point:
            return queryset

        point.srid = distance_srid

        queryset = queryset.annotate(distance=Distance(filter_field, point))
        queryset = queryset.order_by('%s' % 'distance')

        return queryset
