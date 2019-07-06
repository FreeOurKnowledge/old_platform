#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .models import User
from .orcid_wrapper import authorize, obtain_data
from django.conf import settings
import string
import random
import factory



class OrcidBackend:
    def auth_orcid(self, request):
        code = request.GET['code']
        data = authorize(code)
        user, created = User.objects.get_or_create(username=data['orcid'])
        if created:
            user.first_name = data['name']
            user.name = data['name']
            new_data = obtain_data(data['orcid'], data['access_token'])
            user.save()
        return user

    def auth_debug(self, request):
        orcid = ''.join(random.choice(string.ascii_lowercase) for _ in range(10))
        user, created = User.objects.get_or_create(
            username=orcid,
            defaults={
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.first_name = factory.Faker('first_name').generate([])
            user.name = factory.Faker('first_name').generate([])
            user.save()
        return user

    def authenticate(self, request, *args, **kwargs):
        return self.auth_orcid(request) if settings.USE_ORCID else self.auth_debug(request)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
