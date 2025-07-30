from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User

from django.shortcuts import render
from .models import Message


@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Log user out before deleting
    user.delete()  # Triggers post_delete signal
    return redirect("home")  # Redirect after deletion


@login_required
def conversation_view(request):
    # Fetch messages sent or received by the logged-in user
    root_messages = (
        Message.objects.filter(receiver=request.user, parent_message__isnull=True)
        .select_related("sender", "receiver")
        .prefetch_related("replies__sender")
    )

    return render(request, "messaging/conversation.html", {"messages": root_messages})
