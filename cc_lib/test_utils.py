#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_user_fixtures_factory():
    from importlib import import_module
    from django.conf import settings
    path = settings.USER_FIXTURE_FACTORY_CLASS
    s_module, cls = '.'.join(path.split('.')[:-1]), path.split('.')[-1]
    module = import_module(s_module)
    return getattr(module, cls)
