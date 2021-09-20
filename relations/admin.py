from django.contrib import admin

from . import models


@admin.register(models.Relation)
class RelationAdmin(admin.ModelAdmin):
    pass
