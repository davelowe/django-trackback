from django.core.urlresolvers import get_resolver, NoReverseMatch, Resolver404
from django.contrib.sites.models import Site

def decorated(target_url):
    """
    Returns the pinged object, if the view was decorated with the
    ``receives_pingbacks_for`` decorator.
    
    """   
    try:
        urlresolver = get_resolver(None)
        site = Site.objects.get_current()
        func, args, kwargs = urlresolver.resolve(target_url.replace("http://%s"%site.domain, ''))
        
        if hasattr(func, 'pingback_object'):
            obj = func.pingback_object
            return obj
        return None    
    except (NoReverseMatch, Resolver404), e:
        return None        
            

def generic_view(target_url):
    """
    Tries to figure out, of the view is a generic view and determines which
    object is served by the view.
    
    """
    try:
        urlresolver = get_resolver(None)
        site = Site.objects.get_current()
        func, args, kwargs = urlresolver.resolve(target_url.replace("http://%s"%site.domain, ''))
        
        if func.__name__ == 'object_detail':
            # may be django's generic view or something which at least works in an similar fashion
            if 'object_id' in kwargs:
                if 'queryset' in kwargs:
                    try:
                        obj = kwargs['queryset'].get(pk=kwargs['object_id'])
                        return obj
                    except Exception, e:
                        pass
                elif 'model' in kwargs:
                    try:
                        obj = kwargs['model'].objects.get(pk=kwargs['object_id'])
                        return obj
                    except Exception, e:
                        pass
                        
            elif 'slug' in kwargs and 'slug_field' in kwargs:
                try:
                    obj = kwargs['queryset'].get(**{kwargs['slug_field']: kwargs['slug'],})
                    return obj
                except Exception, e:
                    pass
                    
        return None    
    except (NoReverseMatch, Resolver404), e:
        return None
            
