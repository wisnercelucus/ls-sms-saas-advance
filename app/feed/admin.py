from django.contrib import admin

from feed.models import Post, HashTag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    pass