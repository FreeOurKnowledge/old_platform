#!/usr/bin/env python
# -*- coding: utf-8 -*-

from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class MediaStorage(S3Boto3Storage):
    location = settings.EXTERNAL_MEDIA_PATH
    file_overwrite = settings.MEDIA_FILE_OVERWRITE
