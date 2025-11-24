from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'date', 'location', 'price', 'is_past_event']
    list_filter = ['event_type', 'date', 'created_at']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'date'
    ordering = ['-date']