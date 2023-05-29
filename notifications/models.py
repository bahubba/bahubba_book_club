import uuid

from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from book_club.models import Reader, BookClub


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        REGISTERED = 'RG', _('Registered'),
        INVITED_TO_CLUB = 'IN', _('Invited'),
        MEMBERSHIP_REQUESTED = 'MR', _('Membership Requested'),
        MEMBERSHIP_DECLINED = 'MD', _('Membership Declined'),
        MEMBERSHIP_ACCEPTED = 'MA', _('Membership Accepted'),
        NEW_READER = 'NR', _('New Reader'),

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, null=False
    )
    source_reader = models.ForeignKey(Reader, on_delete=models.DO_NOTHING, related_name='source_reader')
    target_reader = models.ForeignKey(Reader, on_delete=models.DO_NOTHING, null=True, related_name='target_reader')
    book_club = models.ForeignKey(BookClub, on_delete=models.DO_NOTHING, null=True)
    type = models.CharField(
        max_length=2,
        choices=NotificationType.choices
    )
    action_link = models.URLField(null=True, blank=True)
    viewed_by = models.ManyToManyField(Reader, through='NotificationViews', related_name='viewed_by')
    generated = models.DateTimeField(default=datetime.now)


class NotificationViews(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.DO_NOTHING)
    reader = models.ForeignKey(Reader, on_delete=models.DO_NOTHING)
    viewed_at = models.DateTimeField(default=datetime.now)
