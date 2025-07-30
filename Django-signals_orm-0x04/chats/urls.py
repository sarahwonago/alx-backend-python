from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework import routers
from django.urls import path, include

from .views import ConversationViewSet, MessageViewSet

# Root router
router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages", MessageViewSet, basename="message")

# Nested router: messages under conversations
conversation_router = NestedDefaultRouter(
    router, r"conversations", lookup="conversation"
)
conversation_router.register(
    r"messages", MessageViewSet, basename="conversation-messages"
)

urlpatterns = [
    path("", include(router.urls)),
    path("", include(conversation_router.urls)),
]
