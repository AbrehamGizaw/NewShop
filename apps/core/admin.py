from os.path import dirname, basename
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

name = basename(dirname(__file__))
models = apps.get_app_config(name).get_models()

for model in models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass

