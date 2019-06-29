#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import DetailView
from django.apps import apps


class CampaignView(DetailView):
    http_method_names = ['get']
    model = apps.get_model('fok', 'Campaign')

    def get_context_data(self, **kwargs):
        from ..models import Pledge
        pledge = Pledge.objects.filter(user=self.request.user, campaign=self.object).first() \
            if not self.request.user.is_anonymous else None
        return super().get_context_data(pledge=pledge)
