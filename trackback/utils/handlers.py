import re
from trackback.utils.send import send_trackback as send_tb, send_pingback as send_pb
from django.contrib.sites.models import Site

URL_RE = re.compile(r'http://[^\ ]+', re.IGNORECASE) # TODO: this is simple+stupid


def send_trackback(instance, **kwargs):
    """
    Default signal handler for sending trackbacks.
    
    Assumes that the ``instance`` has an attribute named 
    ``trackback_content_field_name``, which contains the name of the
    model-field, which should be searched for urls to trackback.
    
    """
    content = getattr(instance, instance.trackback_content_field_name)
    urls = URL_RE.findall(content)
    data = {}
    site = Site.objects.get_current()
    data['url'] = site.domain + instance.get_absolute_url()
    data['title'] = unicode(instance)
    data['blog_name'] = site.name
    data['excerpt'] = content[:100]
    
    for url in urls:
        #print "trackbacking %s" % url
        send_tb(url, data,) # fail_silently=False)
    
    


def send_pingback(instance, **kwargs):
    """
    Default signal handler for sending pingbacks
    
    """
    content = getattr(instance, instance.trackback_content_field_name)
    urls = URL_RE.findall(content)
    for url in urls:
        #print "pingbacking %s" % url
        send_pb(instance.get_absolute_url(), url,)# fail_silently=False)