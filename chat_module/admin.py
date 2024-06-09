from django.contrib import admin
from .models import Message, Room, ConnectionHistory

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'content', 'timestamp']
    list_filter = ['sender', 'receiver', 'timestamp']
    search_fields = ['sender__username', 'receiver__username', 'content']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ['participants']

@admin.register(ConnectionHistory)
class ConnectionHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_id', 'status', 'first_login', 'last_echo']
    list_filter = ['status']
    search_fields = ['user__username', 'device_id']

