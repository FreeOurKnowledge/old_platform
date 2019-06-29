#!/usr/bin/env python
# -*- coding: utf-8 -*-

from constance import config
from collections import namedtuple
from django.conf import settings

OrcidData = namedtuple('OrcidData', 'base_url id redirect_url enabled')


def add_config(request):
    return {
        'config': config,
        'orcid': OrcidData(
            base_url=settings.BASE_ORCID_URL,
            id=settings.ORCID_ID,
            redirect_url=settings.ORCID_REDIRECT_URL,
            enabled=settings.USE_ORCID
        )
    }
