#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from django.conf import settings

# https://members.orcid.org/api/tutorial/read-orcid-records


def authorize(auth_code):
    data = requests.post(
        f'{settings.BASE_ORCID_URL}/oauth/token',
        data={
            'client_id': settings.ORCID_ID,
            'client_secret': settings.ORCID_SECRET,
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': settings.ORCID_REDIRECT_URL
        },
        headers={
            'accept': 'application/json'
        }
    )
    assert data.status_code == 200
    return data.json()


def obtain_data(user_id, token):
    data = requests.get(
        f'{settings.BASE_ORCID_API_URL}/{user_id}/email',
        headers={
            'accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    )
    return data.json()
