from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="edited_messages",
    )
    parent_message = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    is_read = models.BooleanField(default=False)

    objects = models.Manager()  # default manager
    unread = UnreadMessagesManager()

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

    def is_root(self):
        return self.parent_message is None


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="history"
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - Message ID: {self.message.id}"
