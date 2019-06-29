#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.contrib.auth.forms import PasswordChangeForm
from ..forms import UserDataForm, SignPledgeForm
from ..models import Pledge
from django.contrib import messages


class UserProfileView(TemplateView):
    template_name = "fok/user_detail.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            password_change_form=PasswordChangeForm(self.request.user),
            user_data_form=UserDataForm(instance=self.request.user)
        )

    def post(self, request, *args, **kwargs):
        _type = request.POST['type']
        if _type == 'password':
            form = PasswordChangeForm(self.request.user, self.request.POST)
            successful_message = 'Password successfully updated'
        elif _type == 'user_data':
            form = UserDataForm(instance=self.request.user, data=self.request.POST)
            successful_message = 'User data successfully updated'

        if form.is_valid():
            form.save()
            messages.success(request, successful_message)
        else:
            for value in form.errors.values():
                messages.error(request, value.as_text().replace('* ', ''))
        return self.get(request, *args, **kwargs)
