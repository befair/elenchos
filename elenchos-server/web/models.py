# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Subscription(models.Model):

    class Meta:
        verbose_name = 'abbonamento'
        verbose_name_plural = 'abbonamenti'

    # IDRFID stringa da 255 (255 caratteri è indicativo dipende dalle dimensioni dell’ID dell’RFID)  caratteri chiave primaria (codice univoco RFID)
    id_rfid = models.CharField(max_length=256)
    # IDCAUS stringa da 16 caratteri (campo contenente un messaggio da visualizzare)
    welcome_message = models.CharField(max_length=16, default='OK')
    id_user = models.PositiveIntegerField()
    note = models.CharField(max_length=255, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

    def logs_count(self):
        return self.log_set.count()
    logs_count.short_description = 'conteggio accessi'


class Log(models.Model):

    ACTIONS = (
        (0, 'Porta chiusa, LED rosso, doppio beep'),
        (1, 'Porta aperta, LED verde, singolo beep'),
        (2, 'Porta aperta, LED arancio, singolo beep'),
    )

    class Meta:
        verbose_name = 'accesso'
        verbose_name_plural = 'accessi'

    subscription = models.ForeignKey(Subscription, null=True, blank=True)
    id_rfid = models.CharField(max_length=256)
    id_user = models.PositiveIntegerField(null=True, blank=True)
    data = models.CharField(max_length=8)
    ora = models.CharField(max_length=4)
    ts = models.DateTimeField()
    in_out = models.PositiveIntegerField(choices=((0, 'Entrata'), (1, 'Uscita')), default=0)
    action = models.PositiveIntegerField(choices=ACTIONS, default=1)
