# Django-Rest-Framework-Gis-Distance

This is a extension to [Django-Rest-Framework-Gis](https://github.com/djangonauts/django-rest-framework-gis) that adds sorting and distance distance to the [DistanceToPointerFilter](https://github.com/djangonauts/django-rest-framework-gis#distancetopointfilter).


## Requirements

- Python 2.7
- Django 1.7+
- Django-Rest-Framework-Gis 0.10+


## Installation

Install the library with pip:

```
$ pip install djangorestframework-gis-distance
```


## Quick Setup

Make sure `rest_framework_gis_distance` is added to your `INSTALLED_APPS`, after `rest_framework` and `restframework_gis`.

```python
INSTALLED_APPS = (
    # ...

    'rest_framework',
    'rest_framework_gis',
    'rest_framework_gis_distance',
)
```


## Usage


### Regular implementation

First include DistanceField in your serializer.

```python
from restframework_gis_distance.fields import DistanceField

class RecordSerializer(serializers.ModelSerializer):
    distance = DistanceField(unit='m')

    class Meta:
        model = Record
        fields = ('location', 'title', 'created', 'distance')
```


Then use the filter `OrderedDistanceToPointFilter` in your view.

```python
from restframework_gis_distance.filters import OrderedDistanceToPointFilter

class RecordListView(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RecordSerializer
    queryset = Record.objects.all()
    filter_backends = (OrderedDistanceToPointFilter,)
    distance_filter_field = 'location'
    distance_filter_convert_meters = True
    distance_filter_add_distance = True
```

After this, set up your urls as usual and call your endpoint like this:
`example.com/api/endpoint/?dist=1000&point=long,lat`


### Optional field

Using distance as a optional field (for the cases when you only want to display distance when geo coordinates is supplied)

Instead of declaring a straight DistanceField, wrap the DistanceField as a SerializerMethodField, like this:

```python
from restframework_gis_distance.filters import OrderedDistanceToPointFilter

class RecordOptionalSerializer(serializers.ModelSerializer):
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Record
        fields = ('location', 'title', 'created', 'distance')

    def get_distance(self, obj):
        distance = getattr(obj, "distance", None)
        return DistanceField(unit='m').to_representation(distance)
```

## Options

### These belong in your DRF view:

- `distance_filter_field`: Target geo filtering field (inherited from DistanceToPointerFilter).
- `distance_srid`: (Optional) The srid you want to use on your distance. (Default `4326`)
- `distance_sort_order`: (Optional) Indicates the sort order, closest (`True`) or farthest (`False`). (Default: `True`) 


## Questions
- How do I change distance unit?
	- Add the param unit=DESIRED_UNIT to your DistanceField, make sure you use a [django supported unit](https://docs.djangoproject.com/en/1.9/ref/contrib/gis/measure/#supported-units).


## Tests

This library include tests, just run `python runtests.py`.


## Contributing

Want to contribute? Awesome. Just send a pull request.


## License

Django-Rest-Framework-Gis-Distance is released under the [MIT License](http://www.opensource.org/licenses/MIT).

