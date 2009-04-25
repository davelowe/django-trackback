from django import forms
from trackback.models import Trackback


class TrackbackForm(forms.ModelForm):
    class Meta:
        model = Trackback
        exclude = ('content_type', 'object_id', 'content_object', 'remote_ip', 'site', 'submit_date')