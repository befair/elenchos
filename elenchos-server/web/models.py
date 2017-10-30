# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

ACTIONS = (
    (0, 'Porta chiusa, LED rosso, doppio beep'),
    (1, 'Porta aperta, LED verde, singolo beep'),
    (2, 'Porta aperta, LED arancio, singolo beep'),
)


class Subscription(models.Model):

    class Meta:
        db_table = 'subscription'
        verbose_name = 'abbonamento'
        verbose_name_plural = 'abbonamenti'

    ext_user_id = models.PositiveIntegerField(primary_key=True)

    # IDRFID stringa da 255 (255 caratteri è indicativo dipende dalle dimensioni dell’ID dell’RFID)  caratteri chiave primaria (codice univoco RFID)
    rfid = models.CharField(max_length=256)
    # IDCAUS stringa da 16 caratteri (campo contenente un messaggio da visualizzare)
    welcome_msg = models.CharField(max_length=16, default='OK')
    note = models.CharField(max_length=255, blank=True, null=True)

    # LF: non ci andrebbero, sono tutti NULL in questa tabella - sentire cliente
    in_out = models.PositiveIntegerField(choices=((0, 'Entrata'), (1, 'Uscita')), default=0)
    action = models.PositiveSmallIntegerField(choices=ACTIONS, default=1)

    str_date = models.CharField(max_length=8)
    str_time = models.CharField(max_length=6)
    # LF: END non ci andrebbero, sono tutti NULL in questa tabella - sentire cliente
    created_on = models.DateTimeField(auto_now_add=True)

    def logs_count(self):
        return self.log_set.count()
    logs_count.short_description = 'conteggio accessi'


class Log(models.Model):

    class Meta:
        db_table = 'log'
        verbose_name = 'accesso'
        verbose_name_plural = 'accessi'

    ext_user_id = models.ForeignKey(Subscription)

    rfid = models.CharField(max_length=256)
    welcome_msg = models.CharField(max_length=16, default='OK')
    note = models.CharField(max_length=255, blank=True, null=True)

    in_out = models.PositiveIntegerField(choices=((0, 'Entrata'), (1, 'Uscita')), default=0)
    action = models.PositiveIntegerField(choices=ACTIONS)

    str_date = models.CharField(max_length=8)
    str_time = models.CharField(max_length=6)
    created_on = models.DateTimeField(auto_now_add=True)

    # TODO populate data ora in a post_save
