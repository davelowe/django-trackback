from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site



class PingbackUrlInjectionMiddleware(object):
    """
    Adds an X-Pingback header to the response.
    TODO: only add the header to pingbackable resources.
    
    """
    def __init__(self):
        self.site = Site.objects.get_current()
        
    def process_response(self, request, response):
        if not response.has_header('X-Pingback'):
            response['X-Pingback'] = u"http://%s%s" % (self.site.domain, reverse('receive_pingback'))
        return response