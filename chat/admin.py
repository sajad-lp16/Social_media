from django.contrib import admin

from . import models


class MessageInline(admin.TabularInline):
    model = models.Message


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):
    inlines = MessageInline,


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = '__str__', 'create_time',

