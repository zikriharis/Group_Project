from django.contrib import admin
from .models import Share, Bookmark

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaign', 'platform', 'shared_at')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'campaign', 'created_at')