#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from .admin import fok_admin_site
from django.views.generic import TemplateView

from .models import Campaign
from .views import SignPledgeView, UserProfileView, CampaignView, LoginView, NewsletterView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', TemplateView.as_view(
        template_name="fok/home.html",
        extra_context={
            # The lambda makes this expression to be executed each call of home (because of the admin updates)
            'campaigns': lambda: Campaign.objects.filter(visible=True).order_by('position', '-created_at')
        }
    ), name='home'),
    path('admin/', fok_admin_site.urls, name='admin'),
    path('campaign/<slug:slug>', CampaignView.as_view(), name='campaign'),
    path('user/', UserProfileView.as_view(), name='user'),
    path('pledge/<slug:slug>', SignPledgeView.as_view(), name='pledge'),
    path('pledge/<slug:slug>/sign/', SignPledgeView.as_view(), name='sign'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(
        next_page='home'
    ), name='logout'),
    path('newsletter/', NewsletterView.as_view(), name='newsletter')
]
