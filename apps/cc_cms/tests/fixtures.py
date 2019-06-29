#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cc_lib.fixtures import DjangoFactory
from django.apps import apps


class ContentFactory(DjangoFactory):
    class Meta:
        model = apps.get_model('cc_cms', 'Content')


class DynamicTextFactory(DjangoFactory):
    class Meta:
        model = apps.get_model('cc_cms', 'DynamicText')


class ColumnsFactory(DjangoFactory):
    class Meta:
        model = apps.get_model('cc_cms', 'ColumnsSection')


class PageFactory(DjangoFactory):
    class Meta:
        model = apps.get_model('cc_cms', 'Page')

