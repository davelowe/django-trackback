


def receives_pingbacks_for(obj=None, model=None, queryset=None, 
                           object_pk=None, slug=None, slug_field=None):
    """
    A decorator to configure for which object a view should receive 
    pingbacks.
    
    Usage example::
    
        @receives_pingbacks_for(model=BlogEntry, object_pk=15)
        def my_special_view(request):
            ...
            
            
        @receives_pingbacks_for(model=BlogEntry, lookup=...)
    """
    def _decorator(func):
        if obj is not None:
            pingback_object = obj
        else:
            if model is not None:
                if object_pk is not None:
                    pingback_object = model.objects.get(pk=object_pk)
                elif slug is not None and slug_field is not None:
                    pingback_object = model.objects.get(**{"%s"%slug_field:slug})
            elif queryset is not None:
                if object_pk is not None:
                    pingback_object = queryset.get(pk=object_pk)
                elif slug is not None and slug_field is not None:
                    pingback_object = queryset.get(**{"%s"%slug_field:slug})
       
        def _inner(request, *args, **kwargs):
            return func(request, *args, **kwargs)

        if pingback_object:
            _inner.pingback_object = pingback_object
            
        return _inner
    return _decorator