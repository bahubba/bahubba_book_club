import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from book_club.models import Reader, BookClub


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        MEMBERSHIP_REQUESTED = 'MR', _('Membership Requested'),
        MEMBERSHIP_DECLINED = 'MD', _('Membership Declined'),
        MEMBERSHIP_ACCEPTED = 'MA', _('Membership Accepted'),
        NEW_MEMBER = 'NM', _('New Member'),

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, null=False
    )
    notified_readers = models.ManyToManyField(Reader, through='ReaderNotifications')
    source_reader = models.ForeignKey(Reader, on_delete=models.DO_NOTHING, related_name='source_reader')
    book_club = models.ForeignKey(BookClub, on_delete=models.DO_NOTHING)
    type = models.CharField(
        max_length=2,
        choices=NotificationType.choices
    )
    action_link = models.URLField()
    generated = models.DateTimeField(default=timezone.now)


class ReaderNotifications(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.DO_NOTHING)
    notification = models.ForeignKey(Notification, on_delete=models.DO_NOTHING)
    viewed = models.BooleanField(default=False)
