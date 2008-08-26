"""
For a good write-up about template-tags, please see:
http://www.b-list.org/weblog/2006/jun/07/django-tips-write-better-template-tags/
The code in this module is heavily inspired by James Bennett's blog-post.

"""
from django import template
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from trackback.models import Trackback

register = template.Library()




class TrackbackRdfNode(template.Node):
    """
    Include RDF meta data for the given object, so that remote clients can
    discover a trackback url.

    """
    def __init__(self, obj):
        self.obj_name = obj
        
        
    def render(self, context):
        self.object = template.resolve_variable(self.obj_name, context)
        self.object.ct = ContentType.objects.get_for_model(self.object).pk
        return render_to_string('trackback/rdf_include.xml', {'object': self.object, 'SITE_URL': "http://%s" % Site.objects.get_current().domain})

    
def get_trackback_rdf_for(parser, token):
    bits = token.contents.split()
    if len(bits) != 2:
        raise template.TemplateSyntaxError, "get_trackback_rdf_for tag takes exactly one argument"
    return TrackbackRdfNode(bits[1])


get_trackback_rdf_for = register.tag(get_trackback_rdf_for)




     
class TrackbacksNode(template.Node):
    """
    Get a list of ``num`` Trackbacks for ``obj`` into the 
    current template context as ``varname``.
    
    """
    def __init__(self, obj, num, varname):
        self.num, self.varname = num, varname
        self.obj_name = obj
    
    
    def render(self, context):
        self.object = template.resolve_variable(self.obj_name, context)
        context[self.varname] = Trackback.objects.filter(content_type=ContentType.objects.get_for_model(self.object), object_id=self.object.pk).all()[:self.num]
        return ''
  
 
def get_trackbacks_for(parser, token):
    bits = token.contents.split()
    if len(bits) != 5:
        raise template.TemplateSyntaxError, "get_trackbacks tag takes exactly four arguments"
    if bits[3] != 'as':
        raise template.TemplateSyntaxError, "third argument to get_trackbacks tag must be 'as'"
    return TrackbacksNode(bits[1], bits[2], bits[4])
 
    
get_trackbacks_for = register.tag(get_trackbacks_for)



