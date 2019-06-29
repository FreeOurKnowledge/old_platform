from django.contrib import admin
from .models import User, Background, Campaign, Pledge
from cc_cms.admin import register_cms, Page, PageAdmin
from constance.admin import ConstanceAdmin, Config
from django_summernote.admin import SummernoteModelAdmin


class FokAdmin(admin.AdminSite):
    site_header = "Free Our Knowledge"
    site_title = "FOK Admin"


class FokPageAdmin(PageAdmin):
    exclude = ('intro',)


class CampaignAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'


fok_admin_site = FokAdmin(name='fok_admin')
fok_admin_site.register(User)
fok_admin_site.register(Background)
fok_admin_site.register(Campaign, CampaignAdmin)
fok_admin_site.register(Pledge)
fok_admin_site.register([Config], ConstanceAdmin)

register_cms(fok_admin_site)

fok_admin_site.unregister(Page)
fok_admin_site.register(Page, FokPageAdmin)
