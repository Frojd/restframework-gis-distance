# -*- coding: utf-8 -*-

"""
This is an extension to django-restframework-gis that extends on
DistanceToPointFilter and adds sorting by distance.
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
        sorting_order = getattr(view, 'distance_sort_order', True)
        point = self.get_filter_point(request)

        queryset = super(OrderedDistanceToPointFilter, self)\
            .filter_queryset(request, queryset, view)

        if not filter_field:
            return queryset

        if not point:
            return queryset

        point.srid = distance_srid

        queryset = queryset.annotate(distance=Distance(filter_field, point))
        queryset = queryset.order_by('%s%s' % (
            '-' if not sorting_order else '', 'distance')
        )

        return queryset
