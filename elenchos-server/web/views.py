# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


from web.models import Subscription, Log

# TODO: whitelist indirizzi IP abilitati
# DESIDERATA: meccanismo csrf implementato (Arduino fa una GET periodica al server)
@csrf_exempt
def gate_api(request, id_rfid):

    # TODO: accedere solo con una POST

    subscription = Subscription.objects.filter(id_rfid__iexact=id_rfid).first()

    if subscription:
        response = 'OK'
    else:
        response = 'KO'

    now = timezone.now()
    local_time = timezone.localtime(now)

    # TODO: data e ora, ora sono str_date e str_time e vanno
    # valorizzati nella save() del modello
    Log.objects.create(
        subscription=subscription,
        id_rfid=id_rfid,
        id_user=subscription.id_user if subscription else None,
        data=local_time.strftime('%d%m%Y'),
        ora=local_time.strftime('%H%M'),
        ts=now,
        action=1 if subscription else 0,
    )

    # TODO: statuscode per la risposta:
    # 403 negazione permesso
    # 200 successo
    return HttpResponse(response)
