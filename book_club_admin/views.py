from datetime import datetime
from typing import Optional

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .forms import DenyMembershipForm, ApproveMembershipForm
from book_club.models import BookClub, Reader, MembershipRequest
from notifications.models import Notification


@login_required
def book_club_admin(req, book_club_slug):
    """
    Base admin page for managing a book club
    """

    # Get the book club from the DB
    book_club = __get_admin_club_or_none(book_club_slug, req.user.id)

    # If not an admin, redirect to home
    # TODO - Redirect to current page
    if book_club is None:
        return redirect('home')

    return render(
        req,
        'book_club/book_club_admin.html',
        {'book_club': book_club, 'title_suffix': 'Details', 'section': 'details'},
    )


@login_required
def book_club_admin_members(req, book_club_slug):
    """
    Manage membership for book club
    """

    # Get the book club from the DB
    book_club = __get_admin_club_or_none(book_club_slug, req.user.id)

    # If not an admin, redirect to home
    # TODO - Redirect to current page
    if book_club is None:
        return redirect('home')

    return render(
        req,
        'book_club/book_club_admin.html',
        {
            # TODO - filter readers to only those who haven't left
            'book_club': book_club,
            'title_suffix': 'Members',
            'section': 'members',
        },
    )


@login_required
def book_club_admin_membership_requests(req, book_club_slug):
    """
    Approve or deny membership requests
    """

    # Get the book club from the DB
    book_club = __get_admin_club_or_none(book_club_slug, req.user.id)

    # If not an admin, redirect to home
    if book_club is None:
        return redirect('home')

    # Get membership requests for the book club
    requests = MembershipRequest.objects.filter(book_club__id=book_club.id)

    return render(
        req,
        'book_club/book_club_admin.html',
        {
            'book_club': book_club,
            'title_suffix': 'Membership Requests',
            'section': 'membership_requests',
            'requests': requests
        }
    )


@login_required
def book_club_admin_prefs(req, book_club_slug):
    """
    Manage book club preferences
    """

    # Get the book club from the DB
    book_club = __get_admin_club_or_none(book_club_slug, req.user.id)

    # If not an admin, redirect to home
    # TODO - Redirect to current page
    if book_club is None:
        return redirect('home')

    return render(
        req,
        'book_club/book_club_admin.html',
        {
            'book_club': book_club,
            'title_suffix': 'Preferences',
            'section': 'prefs',
        }
    )


@login_required
def book_club_admin_change_role(req, book_club_slug):
    pass


@login_required
def book_club_admin_remove_reader(req, book_club_slug):
    pass


@login_required
def book_club_admin_approve_new_reader(req, book_club_slug):
    """
    Add the requesting reader to the book club
    """

    if req.method == 'POST':
        # Get the book club from the DB, which the authenticated user must be an admin of
        book_club = __get_admin_club_or_none(book_club_slug, req.user.id)

        # If not an admin, redirect to home
        # TODO - Redirect to current page
        if book_club is None:
            return redirect('home')

        # Get the new reader's ID and their new role from the form
        form = ApproveMembershipForm(req.POST)
        if form.is_valid():
            # Get the new reader from the DB and add them to the book club
            new_reader = Reader.objects.get(id=form.cleaned_data['reader_id'])
            book_club.readers.add(new_reader, through_defaults={'club_role': form.cleaned_data['club_role']})
            book_club.save()

            # Get the membership request and mark it as approved
            __evaluate_membership_request(
                reader_id=form.cleaned_data['reader_id'],
                book_club=book_club,
                evaluator=req.user,
                status=MembershipRequest.RequestStatus.ACCEPTED
            )

            # Generate notifications
            notifications = [
                Notification(
                    source_reader=req.user,
                    target_reader=new_reader,
                    book_club=book_club,
                    type=Notification.NotificationType.MEMBERSHIP_ACCEPTED
                ),
                Notification(
                    source_reader=new_reader,
                    book_club=book_club,
                    type=Notification.NotificationType.NEW_READER
                ),
            ]

            Notification.objects.bulk_create(notifications)

            return redirect('book_club:book_club_admin:book_club_admin_membership_requests', book_club_slug=book_club_slug)
        else:
            return redirect('home')


@login_required
def book_club_admin_reject_new_reader(req, book_club_slug):
    """
    Deny the requesting reader access to the book club
    """

    if req.method == 'POST':
        # Get the book club from the DB, which the authenticated user must be an admin of
        book_club = __get_admin_club_or_none(book_club_slug, req.user.id)

        # If not an admin, redirect to home
        # TODO - Redirect to current page
        if book_club is None:
            return redirect('home')

        # Get the new reader's ID and their new role from the form
        form = DenyMembershipForm(req.POST)
        if form.is_valid():
            # Get the membership request and mark it as rejected
            __evaluate_membership_request(
                reader_id=form.cleaned_data['reader_id'],
                book_club=book_club,
                evaluator=req.user,
                status=MembershipRequest.RequestStatus.REJECTED
            )

            # Generate notification
            rejected_reader = Reader.objects.get(id=form.cleaned_data['reader_id'])
            notification = Notification(
                source_reader=req.user,
                target_reader=rejected_reader,
                book_club=book_club,
                type=Notification.NotificationType.MEMBERSHIP_DECLINED,
            )
            notification.save()

            return redirect('book_club:book_club_admin:book_club_admin_membership_requests', book_club_slug=book_club_slug)
        else:
            return redirect('home')


@login_required
def book_club_admin_disband(req, book_club_slug):
    """
    Disband a book club (soft delete)
    """

    # Get the book club from the DB
    # TODO - Only creators should be able to disband groups
    book_club = __get_admin_club_or_none(book_club_slug, req.user.id)

    # If not an admin, redirect to home
    # TODO - Redirect to current page
    if book_club is None:
        return redirect('home')

    # Set the book club to disbanded and redirect to home
    book_club.disbanded = datetime.now()
    book_club.save()

    return redirect('home')


def __get_admin_club_or_none(book_club_slug, user_id):
    book_club: Optional[BookClub]
    try:
        book_club = BookClub.objects.get(
            slug=book_club_slug,
            disbanded__isnull=True,
            readers__id=user_id,
            bookclubreaders__club_role='AD',
            bookclubreaders__left__isnull=True,
        )
    except BookClub.DoesNotExist:
        book_club = None

    return book_club


def __evaluate_membership_request(reader_id, book_club, evaluator, status):
    membership_request = MembershipRequest.objects.get(
        reader_id=reader_id, book_club=book_club
    )
    membership_request.status = status
    membership_request.evaluator = evaluator
    membership_request.evaluated = datetime.now()
    membership_request.save()
