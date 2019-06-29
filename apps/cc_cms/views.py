from django.views import generic
from django.apps import apps


class PageView(generic.DetailView):
    model = apps.get_model('cc_cms', 'Page')

    def get_template_names(self):
        return [f'pages/{self.object.slug}.html', 'cc_cms/page.html']
