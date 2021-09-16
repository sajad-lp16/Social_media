from django.contrib import admin

from . import models


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(models.LikeComment)
class LikeCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(models.LikePost)
class LikePostAdmin(admin.ModelAdmin):
    pass
