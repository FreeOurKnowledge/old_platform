#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path, include
from .views import PageView


urlpatterns = [
    path('<slug:slug>/', PageView.as_view(), name='page'),
    path('summernote/', include('django_summernote.urls')),
]
