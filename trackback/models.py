import datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site




class Trackback(models.Model):
    """
    A received Trackback or Pingback
    As the model is pretty similar to django.contrib.comments.FreeComment
    django-trackback may switch to using it in the future.
    
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True, null=True)
    blog_name = models.CharField(max_length=255, blank=True, null=True)
    excerpt = models.TextField(blank=True, null=True)
    
    remote_ip = models.IPAddressField()
    site = models.ForeignKey(Site)
    is_public = models.BooleanField(default=False)
    submit_date = models.DateTimeField(default=None)
    
    
    def __unicode__(self):
        return u"Trackback from %s" % self.url

    def save(self, *args, **kwargs):
        if self.submit_date is None:
            self.submit_date = datetime.datetime.now()
        super(Trackback, self).save(*args, **kwargs)
        
