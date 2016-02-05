import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.gis.geos import GEOSGeometry

from rest_framework import status
from .models import Record


class ApiOptionalDistanceTest(TestCase):
    def setUp(self):
        self.location = Record.objects.create(
            title='Stockholm, Gamla Stan',
            location=GEOSGeometry(
                'POINT(%(lng)s %(lat)s)' % {
                    'lat': 59.325695, 'lng': 18.071868
                }
            )
        )

    def test_distane(self):
        current_point = {'lat': 59.334666, 'lng': 18.06283}

        url = '%s?dist=10000&point=%s,%s' % (
            reverse('record_test_optional_list'),
            current_point['lng'], current_point['lat'])

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 1)
        self.assertTrue('distance' in json_response[0])
        self.assertTrue(json_response[0]['distance'] != -1)

    def test_no_geo(self):
        url = reverse('record_test_optional_list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)
        self.assertTrue(json_response[0]['distance'] == -1)


class ApiDistanceTest(TestCase):
    def setUp(self):
        self.location = Record.objects.create(
            title='Stockholm, Gamla Stan',
            location=GEOSGeometry(
                'POINT(%(lng)s %(lat)s)' % {
                    'lat': 59.325695, 'lng': 18.071868
                }
            )
        )

    def test_distane(self):
        current_point = {'lat': 59.334666, 'lng': 18.06283}

        url = '%s?dist=10000&point=%s,%s' % (
            reverse('record_test_list'),
            current_point['lng'], current_point['lat'])

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 1)
        self.assertTrue('distance' in json_response[0])
        self.assertTrue(json_response[0]['distance'] != -1)

    def test_no_geo(self):
        url = reverse('record_test_list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ApiSortingTest(TestCase):
    def setUp(self):
        self.locations = [
            Record.objects.create(
                title='Gamla Stan',
                location=GEOSGeometry(
                    'POINT(%(lng)s %(lat)s)' % {
                        'lat': 59.325695, 'lng': 18.071868
                    }
                )
            ),

            Record.objects.create(
                title='Hornstull',
                location=GEOSGeometry(
                    'POINT(%(lng)s %(lat)s)' % {
                        'lat': 59.315189, 'lng': 18.043007
                    }
                )
            ),

            Record.objects.create(
                title='Uppsala',
                location=GEOSGeometry(
                    'POINT(%(lng)s %(lat)s)' % {
                        'lat': 59.858564, 'lng': 17.638927
                    }
                )
            ),

            Record.objects.create(
                title='Kalmar',
                location=GEOSGeometry(
                    'POINT(%(lng)s %(lat)s)' % {
                        'lat': 56.663445, 'lng': 16.356779
                    }
                )
            )
        ]

    def test_distance_stockholm(self):
        point_stockholm = {'lat': 59.334666, 'lng': 18.06283}

        url = '%s?dist=100000&point=%s,%s' % (
            reverse('record_test_list'),
            point_stockholm['lng'], point_stockholm['lat'])

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)
        order_list = ['Gamla Stan', 'Hornstull', 'Uppsala']

        self.assertEqual(len(json_response), len(order_list))
        for idx, order_key in enumerate(order_list):
            self.assertTrue(json_response[idx]['title'] == order_key)

    def test_distance_uppsala(self):
        point_uppsala = {'lat': 59.858564, 'lng': 17.638927}

        url = '%s?dist=100000&point=%s,%s' % (
            reverse('record_test_list'),
            point_uppsala['lng'], point_uppsala['lat'])

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)
        order_list = ['Uppsala', 'Gamla Stan', 'Hornstull']

        self.assertEqual(len(json_response), len(order_list))
        for idx, order_key in enumerate(order_list):
            self.assertTrue(json_response[idx]['title'] == order_key)

        self.assertEqual(json_response[0]['distance'], 0.0)
