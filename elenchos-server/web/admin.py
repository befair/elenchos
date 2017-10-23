# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Subscription, Log

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id_rfid', 'id_user', 'welcome_message', 'logs_count')

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('id_rfid', 'id_user', 'data', 'ora', 'ts', 'action')
