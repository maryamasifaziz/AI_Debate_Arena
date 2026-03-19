from django.contrib import admin
from ..debate.models import DebateRoom, DebateMessage


@admin.register(DebateRoom)
class DebateRoomAdmin(admin.ModelAdmin):
    list_display = ("id","title","owner","created_at")

    search_fields = ("title", "owner__username")
    

@admin.register(DebateMessage)
class DebatMessageAdmin(admin.ModelAdmin):
    list_display = ("id","room","role","created_at")
    list_filter = ("role","created_at")
    search_fields = ("content",)
