import django_filters
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()


class MessageFilter(django_filters.FilterSet):
    sender = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    sent_at__gte = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="gte"
    )
    sent_at__lte = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="lte"
    )

    class Meta:
        model = Message
        fields = ["sender", "sent_at__gte", "sent_at__lte"]
