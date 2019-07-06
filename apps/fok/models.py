from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model
from cc_lib.utils import implement_slug
from django.shortcuts import reverse
from django.contrib.auth.models import UserManager
from constance import config as cons


def upload_path(instance, filename):
    if isinstance(instance, Campaign):
        return 'campaign.image/{0}.png'.format(str(uuid4()), filename)


class CCUserManager(UserManager):
    def create_superuser(self, email, password, **extra_fields):
        return super().create_superuser(email, email, password, **extra_fields)


class Background(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'id'
    objects = CCUserManager()
    username = models.CharField(max_length=20, unique=False)
    name = models.CharField(max_length=150, unique=False)
    background = models.ForeignKey(Background, null=True, on_delete=models.SET_NULL, verbose_name='Research Field')
    newsletter = models.BooleanField(default=False)
    is_greeted = models.BooleanField(default=False)

    @property
    def pledged_campaigns(self):
        return [pledge.campaign for pledge in self.pledges.all()]

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.name


class Campaign(models.Model):
    title = models.CharField(max_length=500)
    slug = models.CharField(max_length=500, editable=False)
    image = models.ImageField(null=True, upload_to=upload_path)
    short_description = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField()
    criteria = models.TextField()
    visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True, editable=False)
    position = models.IntegerField(default=0)

    @property
    def absolute_url(self):
        return reverse('campaign', args=[str(self.slug)])

    def get_pledge_from(self, user):
        return next(iter([pledge for pledge in self.pledges.all() if pledge.user == user]), None)

    @property
    def pledge_url(self):
        return reverse('pledge', args=[str(self.slug)])

    @property
    def stats(self):
        from collections import Counter
        from constance import config

        pledges = self.pledges.all()
        fields = [pledge.user.background for pledge in pledges]
        public_users = [str(pledge.user) for pledge in pledges if pledge.allow_public_name]

        n_pledges = len(pledges)
        n_public_users = len(public_users)
        n_anonymous_users = n_pledges - n_public_users
        n_fields = len(fields)

        fields_percentage = {c[0]: int(c[1]/n_fields * 100) for c in Counter(fields).most_common()}
        anonymous_pledges_percentage = (n_anonymous_users / n_pledges) * 100 \
            if n_anonymous_users != 0 \
            else 0

        if cons.OVERRIDE_SUPPORT_METRICS_TEXT:
            support_metric = cons.OVERRIDE_SUPPORT_METRICS_TEXT
        else:
            support_metric = int((n_public_users + (n_anonymous_users * config.ANONYMOUS_USERS_FACTOR)) / n_pledges * 100) \
                if n_pledges != 0 else 0

        return {
            'public_user_pledges': public_users,
            'research_field_impact': fields_percentage,
            'anonymous_pledges_percentage': f'{anonymous_pledges_percentage:.2f}',
            'support_metric': f'{support_metric:.2f}'
        }

    def __str__(self):
        return self.title


implement_slug(Campaign, 'title')


class EnabledAuthorPosition(models.Model):
    position = models.CharField(max_length=25)

    def __str__(self):
        return self.position


class Pledge(models.Model):
    class Meta:
        ordering = ['created_at']

    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='pledges')
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, related_name='pledges')
    implication = models.FloatField(verbose_name='Threshold')
    author_position = models.ManyToManyField(EnabledAuthorPosition)
    allow_public_name = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{str(self.user)} ({self.user.email}) pledge to {self.campaign.title}'
