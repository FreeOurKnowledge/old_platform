from django.db import models
from uuid import uuid4
from cc_lib.utils import implement_slug, truncate_text


def upload_path(instance, filename):
    if isinstance(instance, Page):
        return 'course.banner/{0}/banner.png'.format(str(uuid4()), filename)


class Content(models.Model):
    text = models.TextField()
    created_on = models.DateTimeField(null=True, blank=True, editable=False)

    def __str__(self):
        return truncate_text(self.text)


class DynamicText(Content):
    name = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return self.name


class Page(Content):
    name = models.CharField(max_length=100, blank=False, unique=True)
    title = models.CharField(max_length=200, blank=False)
    intro = models.TextField(null=True, blank=True)
    slug = models.CharField(max_length=250, unique=True, editable=False)
    thumbnail = models.ImageField(null=True, blank=True, upload_to=upload_path, max_length=250)

    def __str__(self):
        return self.name


implement_slug(Page, 'name')


class Section(models.Model):
    class Meta:
        abstract = True
    SECTION_TYPE = [
        ('NON', 'none'),
        ('COL', 'columns'),
    ]
    name = models.CharField(max_length=200, blank=False, unique=True)
    type = models.CharField(max_length=3, choices=SECTION_TYPE, default='NON')
    content = models.ManyToManyField(Content, blank=True, related_name='sections')

    @staticmethod
    def query(**kwargs):
        subclss = Section.__subclasses__()
        for clss in subclss:
            try:
                obj = clss.objects.get(**kwargs)
            except clss.DoesNotExist:
                continue
            else:
                return obj
        return None

    def __str__(self):
        return self.name


class ColumnsSection(Section):
    type = models.CharField(max_length=3, default='COL')
