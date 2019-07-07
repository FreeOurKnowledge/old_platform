#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import View
from ..forms import NewsletterForm
from django.shortcuts import redirect
from django.contrib import messages


class NewsletterView(View):
    def post(self, request, *args, **kwargs):
        values = request.POST.copy()
        if 'newsletter' in values.keys() and not values['email']:
            messages.error(request, 'You accepted to receive the newsletter, however your email address was not given.')
            return redirect(request.META['HTTP_REFERER'])
        redirect_url = values.pop('redirect_url')[0]
        form = NewsletterForm(instance=request.user, data=values)
        if form.is_valid():
            user = form.save()
            user.is_greeted = True
            user.save()
        return redirect(redirect_url)
