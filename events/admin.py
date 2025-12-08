from django.contrib import admin
from .models import Event, Comment

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'date', 'location', 'price']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'event', 'created_at', 'active']
    list_filter = ['active', 'created_at']