#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .dynamic_text import register
from django.template.loader import render_to_string
from cc_cms.models import Section


def section(section_name):
    the_section = Section.query(name=section_name)
    context = {
        'obj': the_section
    }
    return render_to_string('cc_cms/section.html', context)


register.filter('section', section)
