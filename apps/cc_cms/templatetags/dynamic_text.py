#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import template
from django.template.loader import render_to_string
from cc_cms.models import DynamicText


def dynamic_text(text_name):
    the_text = DynamicText.objects.get(name=text_name)
    context = {
        'obj': the_text
    }
    return render_to_string('cc_cms/dynamic_text.html', context)


register = template.Library()
register.filter('dynamic_text', dynamic_text)
