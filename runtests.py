#!/usr/bin/env python

import sys
from django.conf import settings
from django.core.management import execute_from_command_line


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.contrib.gis.db.backends.postgis',
                'NAME': 'django_restframework_gis',
                'USER': 'postgres',
                'PASSWORD': 'postgres',
                'HOST': '',
                'PORT': ''
            },
        },
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'django.contrib.admin',

            'rest_framework',
            'rest_framework_gis',
            "restframework_gis_distance",
            "tests",
        ),
        MIDDLEWARE_CLASSES=[],
        ROOT_URLCONF="tests.urls"
    )


def runtests():
    argv = sys.argv[:1] + ["test"] + sys.argv[1:]
    execute_from_command_line(argv)


if __name__ == "__main__":
    runtests()
