from rest_framework import permissions
from .models import Message, Conversation


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows only authenticated users who are participants of the conversation
    to access or modify messages or conversations.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        # If this is a message object, check if user is in its conversation
        if isinstance(obj, Message):
            if request.method in ["PUT", "PATCH", "DELETE", "GET"]:
                return user in obj.conversation.participants.all()

        # If this is a conversation object
        if isinstance(obj, Conversation):
            if request.method in ["PUT", "PATCH", "DELETE", "GET"]:
                return user in obj.participants.all()

        return False
