#!/usr/bin/env python
# -*- coding: utf-8 -*-

from factory.django import DjangoModelFactory
import factory
import cc_lib.fixture_helpers as helpers


known_attributes = {
    'address': factory.Faker('address'),
    'date_joined': helpers.one_past_moment_between_days(100, 10),
    'description': factory.Faker('text', max_nb_chars=2000),
    'email': factory.Sequence(lambda n: "user%d@codi.coop" % n),
    'first_name':  factory.Faker('first_name'),
    'is_active': True,
    'is_staff': False,
    'is_superuser': False,
    'last_login': helpers.one_moment_in_the_last_days(10),
    'last_name': factory.Faker('last_name'),
    'name': lambda cls_name: factory.Sequence(lambda n: f'{cls_name} {n}'),
    'password': factory.PostGenerationMethodCall('set_password', 'test'),
    'phone': factory.Faker('phone_number'),
    'text': factory.Faker('text', max_nb_chars=2000),
    'title': factory.Faker('sentence'),
    'url': factory.Faker('url'),
    'username': factory.Sequence(lambda n: "user%d" % n),
    'web': factory.Faker('url'),
}


def set_att_value(cls, field):
    the_field = known_attributes[field.attname]
    the_field = the_field \
        if not hasattr(known_attributes[field.attname], '__call__') \
        else the_field(cls._meta.model.__name__)
    cls._meta.pre_declarations.declarations[field.attname] = the_field
    if hasattr(the_field, 'unroll_context') and hasattr(the_field, 'call'):
        cls._meta.post_declarations.declarations[field.attname] = known_attributes[field.attname]
    setattr(cls, field.attname, the_field)
    cls._meta.base_declarations[field.attname] = the_field


class DjangoFactory(DjangoModelFactory):
    class Meta:
        abstract = True

    @classmethod
    def _generate(cls, strategy, params):
        fields = cls._meta.model._meta.get_fields(True, True)
        for field in fields:
            # is a field that has attname not None and has not been previously declared, then set attribute
            hasattr(field, 'attname') \
                and known_attributes.get(field.attname, None) \
                and not cls._meta.pre_declarations.declarations.get(field.attname, None) \
                and set_att_value(cls, field)
        return super(DjangoFactory, cls)._generate(strategy, params)
