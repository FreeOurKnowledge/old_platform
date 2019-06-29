#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from PIL import Image
from io import BytesIO
from django.forms.widgets import CheckboxInput


class ExtendedImageField(forms.ImageField):
    def __init__(self, resize=None, filename=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize = resize
        self.filename = filename

    def to_python(self, data):
        f = super().to_python(data)
        if not self.resize:
            return f

        byte_array = BytesIO()
        image = Image.open(f)
        # image.show()
        image = image.resize(self.resize)
        image.save(byte_array, format='PNG')
        f.name = self.filename if self.filename else f.name
        f.file = byte_array
        f.content_type = Image.MIME.get(image.format)
        f.image = image
        return f


class SelectMultipleChecks(forms.Widget):
    template_name = 'widgets/multiple_checks.html'

    def __init__(self, *args, choices=(), defaults=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = choices
        self.defaults = defaults

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['choices'] = self.choices
        context['selected'] = [v.pk for v in value] if value else [v.pk for v in self.defaults]
        return context


class SelectMultipleChecksField(forms.Field):
    widget = SelectMultipleChecks

    def __init__(self, *args, choices=(), defaults=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = choices if choices else None
        self.defaults = defaults if defaults else None

    def _get_choices(self):
        return self._choices

    def _set_choices(self, value):
        self._choices = self.widget.choices = value if value else None

    choices = property(_get_choices, _set_choices)

    def _get_defaults(self):
        return self._defaults

    def _set_defaults(self, value):
        self._get_defaults = self.widget.defaults = value if value else None

    defaults = property(_get_defaults, _set_defaults)

    def to_python(self, value):
        import json
        values = json.loads(value)
        i_values = [int(v) for v in values]
        return [choice for choice in self._choices if choice.pk in i_values]

    def validate(self, value):
        assert len(value) > 0

    def valid_value(self, value):
        return value


class SwitchWidget(CheckboxInput):
    input_type = 'checkbox'
    template_name = 'widgets/switch_widget.html'
