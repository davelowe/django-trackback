import xmlrpclib, urllib, urllib2
from trackback.utils.parse import discover_pingback_url, discover_trackback_url




def send_pingback(source, target, fail_silently=True, discover_service_callback=discover_pingback_url):
    """
    Send a XML-RPC pingback to ``target``. Service URL is discovered using
    the supplied ``discover_service_callback``. If ``fail_silently`` is True,
    no exception will be raised, otherwise exceptions are passed trough to the
    caller.
    
    Pingback Specs:
    http://www.hixie.ch/specs/pingback/pingback
    
    pingback.ping('url that pings', 'url that is pinged')
    
    """
    try:
        url = discover_service_callback(target)
        #print url #FIXME: handle relative urls. maybe in the callback function
        if url is not None:
            proxy = xmlrpclib.ServerProxy(url)
            proxy.pingback.ping(source, target)
        return
    except Exception, e:
        if fail_silently:
            return
        else:
            raise e
            
            

def send_trackback(target, data, fail_silently=True, discover_service_callback=discover_trackback_url):
    """
    Send a Trackback to ``target``. Service URL is discovered using the
    supplied ``discover_service_url`` callback. If ``fail_silently`` is True,
    no exception will be raised, otherwise exceptions are passed trough to the
    caller.
    
    Trackback Specs:
    http://www.sixapart.com/pronet/docs/trackback_spec
    
    """
    try:
        url = discover_service_callback(target)
        #print url
        if url is not None:
            #print urllib.urlencode(data)
            resp = urllib2.urlopen(url, urllib.urlencode(data))
            #print resp.read()
        return
    except Exception, e:
        #print e
        if fail_silently:
            return
        else:
            raise e




def send_weblog_update(target, site_name, site_url, fail_silently=True):
    """
    Ping a Weblog directory like Technorati etc. and tell them, 
    that your site was updated. Also works with ping-o-matic - a proxy
    that informs a bunch of other directories to speed up your site.
    
    """
    try:
        proxy = xmlrpclib.ServerProxy(target)
        resp = proxy.weblogUpdates.ping(site_name, site_url)
        #print resp
        return
    except Exception, e:
        if fail_silently:
            return
        else:
            raise e
