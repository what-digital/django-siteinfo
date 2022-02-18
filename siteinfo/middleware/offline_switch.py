import re
from django.conf import settings
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect, HttpResponse
from siteinfo.models import SiteSettings
from django.shortcuts import render_to_response
from django.template.context import RequestContext

class OfflineSwitchMiddleware(object):
    """
    OfflineSwitchMiddleware will return a special view if SiteSettings.active
    is set to False.
    By default the 'siteinfo/offline_page.html' template will be used. But
    if a template matching the current site exists, it will be used.
    e.g 'siteinfo/offline_page-example.com.html'
    """
    
    def __init__(self):
        # same as in RequireLoginMiddleware
        self.login_url = getattr(settings, 'LOGIN_URL', '/accounts/login/' )
        public_urls = []
        if hasattr(settings,'PUBLIC_URLS'):
            public_urls = [re.compile(url) for url in settings.PUBLIC_URLS]
        public_urls += [(re.compile("^%s$" % self.login_url[1:]))]
        self.public_urls = tuple(public_urls)
        
    def process_request(self, request):
        try:
            current = SiteSettings.objects.get_current()
            #print u"current: %s" % current
            if current:
                #print u"current: %s" % current
                is_active = current.is_active_now()
                if is_active or getattr(getattr(request,'user',False),'is_staff', False):
                    return None
                for url in self.public_urls:
                    if url.match(request.path[1:]):
                        return None
                # the site must be offline
                return render_to_response(['siteinfo/offline_page-%s.html' % current.site.domain,
                                           'siteinfo/offline_page.html',],
                          {'text': current.inactive_text,
                           'image': current.inactive_image, 
                           'domain':current.site.domain},
                          context_instance=RequestContext(request))
        except AttributeError:
            return None
        return None