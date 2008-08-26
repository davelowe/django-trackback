"""
You may want to hook this URLconf into your Root-URLconf like this::

    url(r'^trackback/', include('trackback.urls')),
    
"""

from django.conf.urls.defaults import *
from trackback.forms import TrackbackForm


trackback_dict = {
    'form_class': TrackbackForm,
    'template_name': 'trackback/trackback_response.xml',
}


urlpatterns = patterns('trackback.views',
    url(r'^(?P<content_type_id>[\d]+)/(?P<object_id>[\d]+)/$', 'receive_trackback', trackback_dict, name="receive_trackback"),
    url(r'^xml-rpc/$', 'receive_pingback', {}, name="receive_pingback"),
)
