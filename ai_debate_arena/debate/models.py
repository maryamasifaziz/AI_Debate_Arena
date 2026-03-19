from django.conf import settings
from django.db import models

class DebateRoom(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="debate_rooms")
    title = models.CharField(max_length=120, default="My Debate Room")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.owner})"

class DebateMessage(models.Model):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("pro", "Pro Agent"),
        ("con", "Con Agent"),
        ("judge", "Judge Agent"),
        ("system", "System"),
    ]
    room = models.ForeignKey(DebateRoom, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
