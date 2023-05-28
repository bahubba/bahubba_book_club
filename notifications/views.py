from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from book_club.models import BookClub, BookClubReaders
from .forms import NotificationLinkForm
from .models import Notification, NotificationViews


@login_required
def notifications_home(req):
    """
    Page to view notifications\
    """

    # Get all book clubs the reader is an admin for
    admin_book_clubs = BookClub.objects.filter(
        readers__id=req.user.id,
        bookclubreaders__club_role=BookClubReaders.RoleInClub.ADMIN,
    )

    # Get notifications for the reader
    notifications = Notification.objects.filter(
        Q(book_club__in=admin_book_clubs.all()) | Q(target_reader__id=req.user.id),
    )

    return render(req, 'notifications/notifications_home.html', {'notifications': notifications})


@login_required
def toggle_viewed(req, notification_id):
    """
    Create or delete a record showing that the user viewed a notification
    """

    # TODO - Keep record of old views even if toggled to unviewed?
    if req.method == 'POST':
        # Get the notification
        notification = Notification.objects.get(id=notification_id)
        if notification.viewed_by.all().contains(req.user):
            notification.viewed_by.remove(req.user)
        else:
            notification.viewed_by.add(req.user, through_defaults={})

        notification.save()

    return redirect('notifications:notifications')


@login_required
def link(req):
    """
    POST URL for clicking on a notification's link
    """

    if req.method == 'POST':
        # Get the notification ID and the redirect URL from the form
        form = NotificationLinkForm(req.POST)
        if form.is_valid():

            # Get the notification and record that the user viewed it
            notification = Notification.objects.get(id=form.cleaned_data['notification_id'])
            if not notification.viewed_by.contains(req.user):
                notification.viewed_by.add(req.user, through_defaults={})
                notification.save()

            return redirect(form.cleaned_data['redirect_url'])

    # TODO - Default?
