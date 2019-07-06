#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.shortcuts import redirect, reverse
from ..forms import SignPledgeForm
from ..models import Pledge, Campaign
from django.contrib import messages


class SignPledgeView(TemplateView):
    template_name = "fok/pledge_detail.html"

    def get_context_data(self, **kwargs):
        campaign = Campaign.objects.get(slug=kwargs['slug'])
        pledge = campaign.get_pledge_from(self.request.user)
        context = super().get_context_data()
        context['object'] = campaign
        context['pledge'] = pledge
        context['form'] = SignPledgeForm(initial={'author_position': [] if not pledge else pledge.author_position.all()})
        return context

    def post(self, request, *args, **kwargs):
        form = SignPledgeForm(request.POST)
        try:
            if not form.is_valid():
                raise Exception('')
            campaign = Campaign.objects.get(slug=kwargs['slug'])
            pledge = campaign.get_pledge_from(request.user)
            author_position = form.cleaned_data.pop('author_position')
            if pledge is None:
                pledge = Pledge(
                    user=request.user,
                    campaign=campaign,
                    **form.cleaned_data
                )
            else:
                assert form.cleaned_data['implication'] <= pledge.implication
                for attr, value in form.cleaned_data.items():
                    setattr(pledge, attr, value)
            pledge.save()
            pledge.author_position.clear()
            for position in author_position:
                pledge.author_position.add(position)
            messages.success(request, 'The pledge was successfully signed')
            return redirect(reverse('campaign', kwargs={'slug': kwargs['slug']}))
        except Exception as e:
            messages.error(request, 'There was an error and this pledge could not be signed')
            return redirect(reverse('campaign', kwargs={'slug': kwargs['slug']}))
