#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from cc_lib.fixtures import DjangoFactory
from ..models import Background, Campaign, Pledge, EnabledAuthorPosition
import factory
from cc_lib.utils import storage_files
from django.conf import settings


class UserFactory(DjangoFactory):
    class Meta:
        model = get_user_model()


class BackgroundFactory(DjangoFactory):
    class Meta:
        model = Background
    name = factory.Iterator(['Mathematics', 'Biology', 'Neuroscience', 'Physics', 'Chemistry', 'Astronomy'])


class CampaignFactory(DjangoFactory):
    class Meta:
        model = Campaign
    visible = True
    criteria = factory.Faker('text', max_nb_chars=2000)
    image = 'https://www.emacswiki.org/pics/static/KitchenSinkBW.png'
    # factory.fuzzy.FuzzyChoice(
    #     storage_files(
    #         settings.FIXTURES_PATH_TO_COVER_IMAGES,
    #         f'http://{settings.AWS_S3_CUSTOM_DOMAIN}/{settings.AWS_STORAGE_BUCKET_NAME}'
    #     )
    #)


class EnabledAuthorPositionFactory(DjangoFactory):
    class Meta:
        model = EnabledAuthorPosition


class PledgeFactory(DjangoFactory):
    class Meta:
        model = Pledge
