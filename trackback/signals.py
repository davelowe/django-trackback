"""
This module includes signals for sending pingbacks and trackbacks. Models
which should trigger the sending of pingbacks and/or trackbacks can send
this signals in their save() methods or an ModelAdmin can send this signals
after successfully publishing an object.

Using this signals is optional. The sender could also call the signal-handler
functions (found in trackback.utils.handlers) or the utility functions (found
in trackback.utils.send) directly.

Please see INSTALL.txt for more information.

"""
from django.dispatch import Signal

send_trackback = Signal(providing_args=["instance"])

send_pingback = Signal(providing_args=["instance"])