from django.db.models.signals import post_save
from django.dispatch import receiver, pre_save
from .models import Message, Notification, MessageHistory
from django.utils import timezone


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return  # It's a new message; no edit to track

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return  # Should not happen, but just in case

    # Check if content changed
    if old_message.content != instance.content:
        # Set the edited flag and timestamp
        instance.edited = True
        instance.edited_at = timezone.now()

        # Copy old content into MessageHistory
        MessageHistory.objects.create(
            message=instance,
            old_content=old_message.content,
            edited_by=instance.edited_by,
        )
