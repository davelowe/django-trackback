from django.contrib import admin
from trackback.models import Trackback


class TrackbackAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'content_type', 'object_id', 'url', 'remote_ip', 'submit_date')
    list_filter = ('content_type', 'object_id', 'remote_ip')
    search_fields = ('object_id', 'remote_ip', 'url')
    date_hierarchy = 'submit_date'
    
admin.site.register(Trackback, TrackbackAdmin)