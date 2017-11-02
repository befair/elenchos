# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Subscription, Log, WhitelistedIP

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('rfid', 'ext_user_id', 'welcome_msg', 'action', 'logs_count')

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('rfid', 'ext_user_id', 'str_date', 'str_time', 'created_on', 'action')

@admin.register(WhitelistedIP)
class WhitelistedIPAdmin(admin.ModelAdmin):
    list_display = ('ip',)


admin.site.site_header = 'Amministrazione Elenchos'
admin.site.index_title = 'Amministrazione Elenchos'
admin.site.site_title = 'Amministrazione Elenchos'

