#!/usr/bin/env python
# -*- coding: utf-8 -*-

from factory import fuzzy
from django.utils import timezone
import datetime


def one_moment_in_the_last_days(days):
    return fuzzy.FuzzyDateTime(
        start_dt=timezone.now() - datetime.timedelta(days=days),
        end_dt=timezone.now()
    )


def one_past_moment_between_days(start_days, end_days):
    return fuzzy.FuzzyDateTime(
        start_dt=timezone.now() - datetime.timedelta(days=start_days),
        end_dt=timezone.now() - datetime.timedelta(days=end_days)
    )


def one_moment_in_the_next_days(days):
    return fuzzy.FuzzyDateTime(
        start_dt=timezone.now(),
        end_dt=timezone.now() + datetime.timedelta(days=days)
    )


def one_future_moment_between_days(start_days, end_days):
    return fuzzy.FuzzyDateTime(
        start_dt=timezone.now() + datetime.timedelta(days=start_days),
        end_dt=timezone.now() + datetime.timedelta(days=end_days)
    )
