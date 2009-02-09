from trackback.models import Trackback
from trackback.forms import TrackbackForm
from trackback import registry
from xmlrpclib import Fault
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher

from django.core.urlresolvers import get_resolver, NoReverseMatch, Resolver404
from django.contrib.sites.models import Site




PINGBACK_SOURCE_DOES_NOT_EXIST = 0x0010
PINGBACK_SOURCE_DOES_NOT_LINK  = 0x0011
PINGBACK_TARGET_DOES_NOT_EXIST = 0x0020
PINGBACK_TARGET_CANNOT_BE_USED = 0x0021
PINGBACK_ALREADY_REGISTERED    = 0x0030
PINGBACK_ACCESS_DENIED         = 0x0031
PINGBACK_UPSTREAM_ERROR        = 0x0032
PINGBACK_OK                    = 'OK'




class PingbackXMLRPCDispatcher(SimpleXMLRPCDispatcher):
    """
    A simple XML-RPC dispatcher that handles Pingbacks.
    
    """
    def _dispatch(self, method, params, request=None):
        method = method.replace('.', '_')
        try:
            # We are forcing the 'handle_' prefix on methods that are
            # callable through XML-RPC to prevent potential security
            # problems
            func = getattr(self, 'handle_' + method)
        except AttributeError:
            raise Exception('method "%s" is not supported' % method)
        else:
            return func(request=request, *params)
        

    def handle_pingback_ping(self, source, target, request=None):
        """
        Handles a Pingback (called via XML-RPC), receives the following parameters:
    
            ``source``: the remote url pinging us
        
            ``target``: our url which is pinged.
        
        Before saving the Pingback as a ``Trackback``-Object, the correct object
        is determined from the ``target``-url
    
        The big problem with pingbacks is to determine the target_object for which
        we receive an pingback because we only get the url on our site.
        If there a multiple objects on the page it's impossible.
        Also if there is only one object at the given url it may be impossible to
        figure which object it is only given the url. 
        Below we first check if it is possible to figure out the object from the
        kwargs of the view function (which works at least for django's generic
        views). If this doesn't work we have to use a user-supplied callback
        function (TODO).
    
        """
       
        if request is None:
            raise Fault(faultCode=PINGBACK_UPSTREAM_ERROR, faultString='PINGBACK_UPSTREAM_ERROR')
        
        obj = None
        
        for resolver in registry.resolvers:
            try:
                obj = resolver(target)
                if obj is not None:
                    break
            except:
                pass
                
        #if not content_object is found raise an exception
        if obj is None:
            #raise Fault(faultCode=PINGBACK_TARGET_CANNOT_BE_USED, faultString='PINGBACK_TARGET_CANNOT_BE_USED')
            raise Fault(faultCode=PINGBACK_TARGET_DOES_NOT_EXIST, faultString='PINGBACK_TARGET_DOES_NOT_EXIST')

        ping = Trackback.objects.create(url=source, 
                                        content_object=obj, 
                                        remote_ip=request.META['REMOTE_ADDR'],
                                        site=Site.objects.get_current())
        if ping:
            return PINGBACK_OK
        #FIXME: wrong error
        raise Fault(faultCode=PINGBACK_ALREADY_REGISTERED, faultString='PINGBACK_ALREADY_REGISTERED')
    



#Instanciate the dispatcher (to be used by the django view function)    
try:
    xmlrpc_dispatcher = PingbackXMLRPCDispatcher(allow_none=False, encoding=None)
except:
    xmlrpc_dispatcher = PingbackXMLRPCDispatcher() #python 2.4


    
    