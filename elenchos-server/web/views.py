# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.utils import timezone

from web.models import Subscription, Log


def gate_api(request, id_rfid):

    subscription = Subscription.objects.filter(id_rfid__iexact=id_rfid).first()

    if subscription:
        response = 'OK'
    else:
        response = 'KO'

    now = timezone.now()
    local_time = timezone.localtime(now)

    Log.objects.create(
        subscription=subscription,
        id_rfid=id_rfid,
        id_user=subscription.id_user if subscription else None,
        data=local_time.strftime('%d%m%Y'),
        ora=local_time.strftime('%H%M'),
        ts=now,
        action=1 if subscription else 0,
    )

    return HttpResponse(response)
