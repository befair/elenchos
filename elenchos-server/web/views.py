# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


from .decorators import ip_whitelisted
from web.models import Subscription, Log


# DESIDERATA: meccanismo csrf implementato (Arduino fa una GET periodica al server)
@require_http_methods(["POST"])
@csrf_exempt
@ip_whitelisted
def gate_api(request, id_rfid):

    subscription = Subscription.objects.filter(rfid__iexact=id_rfid).first()

    if subscription:
        response = subscription.welcome_msg
        if subscription.action == 0:
            status_code = 403
        if subscription.action == 1:
            status_code = 200
        if subscription.action == 2:
            status_code = 402
    else:
        response = 'ACCESSO NEGATO'
        status_code = 403

    now = timezone.now()
    local_time = timezone.localtime(now)

    new_log = Log(
        ext_user_id=subscription,
        rfid=id_rfid,
        created_on=now,
        action=subscription.action if subscription else 0,
    )
    new_log.save()

    return HttpResponse(response, status=status_code)
