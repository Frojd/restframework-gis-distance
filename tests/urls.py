from django.conf.urls import url
from views import RecordOptionalListView, RecordListView


urlpatterns = [
    url(r'^test/records/$', RecordListView.as_view(),
        name='record_test_list'),
    url(r'^test/records-optional/$', RecordOptionalListView.as_view(),
        name='record_test_optional_list'),
]
