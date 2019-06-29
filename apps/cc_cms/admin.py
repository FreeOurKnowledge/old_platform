from django_summernote.admin import SummernoteModelAdmin
from .models import Page, ColumnsSection, Content, DynamicText


class PageAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'


def register_cms(admin_site):
    admin_site.register(Page, PageAdmin)
    admin_site.register(ColumnsSection, PageAdmin)
    admin_site.register(Content, PageAdmin)
    admin_site.register(DynamicText, PageAdmin)
