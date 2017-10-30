# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

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

    str_date = models.CharField(max_length=8, blank=True, null=True)
    str_time = models.CharField(max_length=6, blank=True, null=True)
    # LF: END non ci andrebbero, sono tutti NULL in questa tabella - sentire cliente
    created_on = models.DateTimeField(auto_now_add=True)

    def logs_count(self):
        return self.log_set.count()
    logs_count.short_description = 'conteggio accessi'

    def __unicode__(self):
        return "{} - {}".format(self.ext_user_id, self.rfid)


class Log(models.Model):

    class Meta:
        db_table = 'log'
        verbose_name = 'accesso'
        verbose_name_plural = 'accessi'

    ext_user_id = models.ForeignKey(Subscription, null=True, blank=True)

    rfid = models.CharField(max_length=256)
    welcome_msg = models.CharField(max_length=16, default='OK')
    note = models.CharField(max_length=255, blank=True, null=True)

    in_out = models.PositiveIntegerField(choices=((0, 'Entrata'), (1, 'Uscita')), default=0)
    action = models.PositiveIntegerField(choices=ACTIONS)

    str_date = models.CharField(max_length=8, blank=True)
    str_time = models.CharField(max_length=6, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        local_time = timezone.localtime(self.created_on)
        self.str_date = local_time.strftime('%d%m%Y')
        self.str_time = local_time.strftime('%H%M%S')
        super(Log, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{} - {}".format(self.rfid, self.created_on)


class WhitelistedIP(models.Model):

    class Meta:
        db_table = 'whitelisted_ip'
        verbose_name = 'indirizzo IP consentito'
        verbose_name_plural = 'indirizzi IP consentiti'

    ip = models.GenericIPAddressField(protocol='IPv4')

    def __unicode__(self):
        return "{}".format(self.ip)
