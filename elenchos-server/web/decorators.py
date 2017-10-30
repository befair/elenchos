# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseForbidden

from .models import WhitelistedIP


def ip_whitelisted(function):
    """
    Decorator for the view to check that the client IP is in the whitelist
    """
    def decorator(request, *args, **kwargs):
        ip = request.META['REMOTE_ADDR']
        if WhitelistedIP.objects.filter(ip=ip).exists():
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    decorator.__doc__ = function.__doc__
    decorator.__name__ = function.__name__
    return decorator
