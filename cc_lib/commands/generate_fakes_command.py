#!/usr/bin/env python
# -*- coding: utf-8 -*-

# From: https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/

from django.core.management.base import BaseCommand
from django.core.management.commands.flush import Command as Flush
from django.db import DEFAULT_DB_ALIAS
from django.conf import settings
from cc_lib.utils import get_class_from_route
import inspect
import random
import factory
from factory import fuzzy


relationship_strategies = {
    'choice': (lambda **kwargs: fuzzy.FuzzyChoice(kwargs['objects']), False),
    'sample': (lambda **kwargs: random.sample(kwargs['objects'], kwargs['number']), True),
    'iterate': (lambda **kwargs: factory.Iterator(kwargs['objects']), False)
}


class GenerateFakesCommand(BaseCommand):
    help = 'Generates fake data for all the models, for testing purposes.'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.factories_dict = {}
        self.factory_by_models = {}

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush', '--flush', action='store_true', dest='flush'
        )

    def generated_fake_data(self, objects, model, factory_obj):
        pass

    def fakes_generation_finished(self):
        pass

    def get_image_fields(self, factory_class):
        from django.db.models.fields.files import ImageFileDescriptor
        return [f[0] for f in inspect.getmembers(factory_class._meta.model) if isinstance(f[1], ImageFileDescriptor) and f[0] in factory_class._meta.declarations.keys()]

    def get_related_data(self, factory_cls, related):
        related_instances = {}
        lazy_related = {}
        if related:
            for field_name, values in related.items():
                relationship_field = getattr(factory_cls._meta.model, field_name)
                to_class = relationship_field.field.related_model._meta.label.split('.')[-1]
                assert to_class in self.factory_by_models.keys(), \
                    f"""
                    You have to generate {to_class} fixtures, before {cls_name} fixtures for assigning them 
                    to the {field_name} field.
                    """
                related_objects = self.get_generated_objects(to_class)
                strategy = values.get('strategy', 'iterate')
                strategy, many = relationship_strategies[strategy]
                dest = lazy_related if many else related_instances
                dest[field_name] = strategy(objects=related_objects, **values)
        return related_instances, lazy_related

    def create_data(self, factory_cls, number=50, related=None, fields_value=None, field_values=None, extra_objects=None):
        """

        :param factory_cls:
        :param number:
        :param related:
        :param fields_value: It is an object with the same property name than the fixture. It will set that value on the created fixtures.
        :param field_values: It is a list of values for field names. It will iterate over those values and set them on the created fixtures.
        :param extra_objects:
        :return:
        """
        cls_name = factory_cls._meta.model.__name__
        related_instances, lazy_related = self.get_related_data(factory_cls, related)
        field_values_to_assign = {} if field_values is None else \
            {field_name: factory.Iterator(values) for field_name, values in field_values.items()}
        fields_value = {} if not fields_value else fields_value
        objects = factory_cls.create_batch(
            size=number,
            **fields_value,
            **field_values_to_assign,
            **related_instances
        )
        for field_name, related_objs in lazy_related.items():
            for obj in objects:
                collection = getattr(obj, field_name)
                collection.set(related_objs)
                obj.save()
        self.stdout.write(self.style.SUCCESS(f'Fake data ({number} objects) for {cls_name} model created.'))
        self.generated_fake_data(objects, cls_name, factory_cls)

        if extra_objects:
            for data in extra_objects:
                objects = objects + self.create_data(factory_cls, **data)

        return objects

    def download_and_upload_images(self, objects, fields):
        import urllib.request as request
        import tempfile
        from django.core.files import File

        def _download_and_upload_images(obj, prop):
            if getattr(obj, prop) is None:
                return
            url = str(getattr(obj, prop))
            response = request.urlopen(url)
            data = response.read()
            fp = tempfile.TemporaryFile()
            fp.write(data)
            fp.seek(0)
            setattr(obj, prop, File(fp))
            obj.save()

        for field in fields:
            [_download_and_upload_images(obj, field) for obj in objects]
            len(objects) > 0 and self.stdout.write(
                self.style.SUCCESS(f'Updated {field} field image for model {str(objects[0].__class__.__name__)}.')
            )

    def get_generated_objects(self, cls):
        related_factory = self.factory_by_models[cls]
        return self.factories_dict[related_factory]['objects']

    def get_from_yml(self, path):
        import yaml
        with open(path) as ymlfile:
            yml_string = ymlfile.read()
        return yaml.load(yml_string)

    def handle(self, *args, **options):
        should_ask = not options['flush']
        Flush().handle(interactive=should_ask, database=DEFAULT_DB_ALIAS, **options)
        assert hasattr(settings, 'FIXTURE_FACTORIES'), """
        You should define FIXTURE_FACTORIES list into the settings file before creating fixtures. 
        """
        factories = settings.FIXTURE_FACTORIES \
            if isinstance(settings.FIXTURE_FACTORIES, dict) \
            else self.get_from_yml(settings.FIXTURE_FACTORIES)
        self.factories_dict = {}
        self.factory_by_models = {}
        have_images_list = []
        for factory_class_route, factory_obj in factories.items():
            factory_class = get_class_from_route(factory_class_route)
            cls_name = factory_class._meta.model.__name__
            fnc = getattr(self, 'create_' + cls_name.lower() + 's', self.create_data)
            factory_obj = factory_obj if factory_obj is not None else {}
            objects = fnc(factory_class, **factory_obj)
            self.factory_by_models[cls_name] = factory_class_route
            self.factories_dict[factory_class_route] = {
                'objects': objects,
                'factory': factory_class
            }
            image_fields = self.get_image_fields(factory_class)
            len(image_fields) > 0 and have_images_list.append((objects, image_fields))
        [self.download_and_upload_images(*elements_with_images) for elements_with_images in have_images_list]
        self.fakes_generation_finished()
