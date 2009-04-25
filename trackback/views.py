from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.functional import curry
from django.views.decorators.http import require_POST
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from trackback.pingback import xmlrpc_dispatcher




@require_POST
def receive_trackback(request, content_type_id, object_id, form_class, template_name):
    """
    Endpoint to receive a trackback for any of our objects, described by
    ``content_type_id`` together with ``object_id``.
    
    """
    ctype = get_object_or_404(ContentType, pk=content_type_id)
    obj = get_object_or_404(ctype.model_class(), pk=object_id)
    site = Site.objects.get_current()
    
    form = form_class(request.POST)
    if form.is_valid():
        trackback = form.save(commit=False)
        trackback.content_object = obj
        trackback.remote_ip = request.META['REMOTE_ADDR']
        trackback.site = site
        trackback.save()
        return render_to_response(template_name, {'error': False}, mimetype="text/xml")
    else:
        context = {'error': True,
                   'message': "\n".join(form.errors)
                  }
        return render_to_response(template_name, context, mimetype="text/xml")
    
    


def receive_pingback(request):
    """
    Handles XML-RPC Pingbacks.
    Spec: http://www.hixie.ch/specs/pingback/pingback
    Also see: http://code.djangoproject.com/wiki/XML-RPC
    
    """
    if request.method == 'POST' and len(request.POST):
        try:
            response = HttpResponse(
                            xmlrpc_dispatcher._marshaled_dispatch(
                                        request.raw_post_data, 
                                        dispatch_method=curry(xmlrpc_dispatcher._dispatch, request=request)
                            )
                        )
        except Exception, e:
            #print e
            raise e #FIXME: handle errors gracefully if possible
        
        return response
    return HttpResponse(xmlrpc_dispatcher.system_listMethods(), content_type="'text/plain; charset=utf-8")
    
    
   
   