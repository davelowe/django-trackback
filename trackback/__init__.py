"""
django-trackback - Handle trackbacks and pingbacks in every django-project

"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


DEFAULT_PINGBACK_RESOLVERS = (
    'trackback.utils.resolvers.decorated',
    'trackback.utils.resolvers.generic_view',
)


class ResolverRegistry(object):
    """
    Maintains a list of resolvers used to figure out, which object a
    Pingback should be attached to.
    
    """
    resolvers = []
    
    def __init__(self):
        """
        Initialize the registry with a set of resolvers. Either from 
        ``settings.PINGACK_RESOLVERS`` or from the ``DEFAULT_PINGBACK_RESOLVERS``
        tuple.
        
        """
        resolver_list = getattr(settings, 'PINGBACK_RESOLVERS', DEFAULT_PINGBACK_RESOLVERS)
        for resolver in resolver_list:
            self.add(resolver)
    
            
    def add(self, resolver, first=False):
        """
        Add a resolver to the list. If ``first`` is True, the resolver is
        added at the beginning of the list, otherwise at the end.
        
        """
        if isinstance(resolver, basestring):
            self._import(resolver)
        
        elif callable(resolver):
            if first:
                self.resolvers.insert(0, resolver)
            else:
                self.resolvers.append(resolver)
        
        else:
            raise ImproperlyConfigured("%s isn't callable and not importable as pingback resolver" % resolver)
            
            
    def _import(self, resolver):
        """
        Given a string, tries to import the module and add the specified
        resolver function.
        
        """
        try:
            dot = resolver.rindex('.')
        except ValueError:
            raise ImproperlyConfigured("%s isn't a valid pingback resolver module" % resolver)
        
        r_module, r_funcname = resolver[:dot], resolver[dot+1:]
        
        try:
            mod = __import__(r_module, {}, {}, [''])
        except ImportError, e:
            raise ImproperlyConfigured("Error importing pingback resolver %s: %s" % (resolver, e))
        
        try:
            resolver_func = getattr(mod, r_funcname)
        except AttributeError:
            raise ImproperlyConfigured("Module %s doesn't define a function %s" % (r_module, r_funcname))
        
        self.add(resolver_func)
        
            
            
registry = ResolverRegistry()
