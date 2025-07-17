from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    This can be used to add additional fields or methods specific to the messaging application.
    """
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

class Conversation(models.Model):
    """
    Model representing a conversation between users.
    Each conversation can have multiple participants.
    """
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} with {self.participants.count()} participants"
    

class Message(models.Model):
    """
    Model representing a message sent in a conversation.
    Each message is linked to a specific conversation and has a sender.
    """
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages_sent', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message {self.id} from {self.sender.username} in Conversation {self.conversation.id}"
