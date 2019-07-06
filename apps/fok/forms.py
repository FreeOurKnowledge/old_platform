#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .models import Pledge, User, EnabledAuthorPosition
from django import forms
from cc_lib.form_fields import SelectMultipleChecksField, SwitchWidget


class SignPledgeForm(forms.ModelForm):
    class Meta:
        model = Pledge
        fields = ['implication', 'author_position', 'allow_public_name']
    implication = forms.DecimalField(max_value=100, min_value=0, label='Threshold')
    author_position = SelectMultipleChecksField()
    allow_public_name = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        self.base_fields['author_position'].choices = EnabledAuthorPosition.objects.all()
        self.base_fields['author_position'].defaults = [EnabledAuthorPosition.objects.all().first()]
        super().__init__(*args, **kwargs)


class UserDataForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'newsletter']
        widgets = {
            'newsletter': SwitchWidget
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'newsletter']
        widgets = {
            'newsletter': SwitchWidget
        }
