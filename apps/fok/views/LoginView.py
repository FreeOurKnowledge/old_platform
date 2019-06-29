#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate, login as auth_login
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.conf import settings
from django.shortcuts import redirect


class LoginView(TemplateView):
    template_name = 'fok/login.html'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        user = authenticate(request)
        auth_login(request, user=user)
        if not settings.USE_ORCID:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
