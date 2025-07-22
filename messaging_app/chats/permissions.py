from rest_framework.permissions import BasePermission


class IsParticipant(BasePermission):
    """
    Allows access only to participants of a conversation.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()
