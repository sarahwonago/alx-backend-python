from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, and retrieving conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at'] 
    ordering = ['-created_at']  # Default ordering


    def get_queryset(self):
        # Return conversations that the authenticated user participates in
        return self.queryset.filter(participants=self.request.user).distinct()

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=['post'], url_path='add-message')
    def add_message(self, request, pk=None):
        """
        Custom endpoint to send a message to this conversation.
        """
        conversation = self.get_object()
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user, conversation=conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'sent_at']
    ordering = ['-created_at']


    def get_queryset(self):
        # Return messages from conversations the user participates in
        return self.queryset.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        # Prevent direct assignment to conversations the user isn't part of
        conversation = serializer.validated_data['conversation']
        if not conversation.participants.filter(pk=self.request.user.pk).exists():
            raise PermissionError("You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)
