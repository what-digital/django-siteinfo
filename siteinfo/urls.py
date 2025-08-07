
from django.urls import re_path

from django.conf import settings

from siteinfo.models import SiteSettings

site_settings = SiteSettings.objects.get_current()

if site_settings:
    agb_url = 'http://%s%s%s' % (site_settings.site.domain, settings.MEDIA_URL, site_settings.gtc)
else:
    agb_url = ""


urlpatterns = [
    re_path(r'^login/$', 'django.contrib.auth.views.login', name='login_url'),
    re_path(r'^logout/$', 'django.contrib.auth.views.logout', name='logout_url'),
    re_path(r'^agb/?$', "django.views.generic.simple.redirect_to", {'url': agb_url}, name="agb"),
    re_path(r'^srs/?$', 'siteinfo.views.set_redirect_stop', name='set_redirect_stop'),
    re_path(r'^test_offline_page/?$', 'siteinfo.views.test_offline_page', name='siteinfo-test_offline_page'),
]
