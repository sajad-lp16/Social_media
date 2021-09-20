from django.contrib import admin

from . import models


class MediaTabular(admin.TabularInline):
    model = models.Media


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [MediaTabular]


@admin.register(models.Media)
class MediaAdmin(admin.ModelAdmin):
    pass
