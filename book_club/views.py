from datetime import datetime
from typing import Optional
from urllib.parse import unquote

from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

from notifications.models import Notification
from .models import BookClub, Reader, MembershipRequest, BookClubReaders
from .forms import BookClubForm, ReaderCreationForm, BookClubSearchForm, MembershipRequestForm, ApproveMembershipForm, \
    DenyMembershipForm


def register_reader(req):
    """
    Reader (User) register view and POST
    """

    # TODO - Probably need custom form...
    return_dict = {'form': ReaderCreationForm}

    # Create user on POST
    if req.method == 'POST':
        if req.POST['password1'] == req.POST['password2']:
            try:
                # Create and persist the Reader (User) and log in
                reader = Reader.objects.create_user(
                    username=req.POST['username'],
                    email=req.POST['email'],
                    password=req.POST['password1'],
                    given_name=req.POST['given_name'],
                    surname=req.POST['surname'],
                )
                reader.save()
                login(req, reader)

                # Generate a welcome notification
                notification = Notification(
                    source_reader=req.user,
                    target_reader=req.user,
                    type=Notification.NotificationType.REGISTERED,
                )
                notification.save()

                return redirect('home')
            except IntegrityError:
                return_dict['error'] = 'Username or email has already been taken'

        else:
            return_dict['error'] = 'Passwords do not match'

    # Default to assuming GET functionality

    # If already logged in, redirect
    if req.user.is_authenticated:
        return redirect('home')

    # Otherwise render the register page
    return render(req, 'book_club/register_reader.html', return_dict)


def login_reader(req):
    """
    Login view and POST
    """

    # TODO - Custom login form? Should be able to log in with username OR email
    return_dict = {'form': AuthenticationForm()}

    # Log in on POST
    if req.method == 'POST':
        reader = authenticate(
            req, username=req.POST['username'], password=req.POST['password']
        )
        if reader is None:
            return_dict['error'] = 'Username or password incorrect'
        else:
            login(req, reader)
            return redirect('home')

    # Default to assuming GET functionality

    # If already logged in, redirect
    if req.user.is_authenticated:
        return redirect('home')

    # Otherwise render the login page
    return render(req, 'book_club/login_reader.html', return_dict)


@login_required
def logout_reader(req):
    if req.method == 'POST':
        logout(req)
        return redirect('login')


@login_required
def home(req):

    # Pull the groups the reader is a member of
    reader_clubs = BookClub.objects.filter(readers__id=req.user.id, disbanded__isnull=True).all()
    return_dict = {'book_clubs': reader_clubs, 'in_clubs': len(reader_clubs) > 0}

    return render(req, 'book_club/home.html', return_dict)


@login_required
def book_clubs(req):
    """
    View with readers' book clubs
    """

    # Pull the groups the reader is a member of
    reader_clubs = BookClub.objects.filter(readers__id=req.user.id, disbanded__isnull=True).all()
    # TODO - Is there a different way to do in_clubs' logic in the template?
    return_dict = {'book_clubs': reader_clubs, 'in_clubs': len(reader_clubs) > 0}

    return render(req, 'book_club/book_clubs.html', return_dict)


@login_required
def create_book_club(req):
    """
    Create new book club view and POST
    """

    return_dict = {'form': BookClubForm}

    # Create new book club on POST
    if req.method == 'POST':
        try:
            form = BookClubForm(req.POST, req.FILES)
            # NOTE - Have to persist to get a PK before adding many-to-many related fields
            #        even if you manually create a PK on instantiation... Not cool...
            new_book_club = form.save()
            # TODO - Add slug to the form in the template
            #        ... this means figuring out how to track one field's input value and use it in another
            new_book_club.slug = slugify(new_book_club.name)
            new_book_club.readers.add(req.user, through_defaults={'club_role': 'AD', 'is_creator': True})
            new_book_club.save()

            return redirect('book_club:book_clubs')
        except IntegrityError:
            return_dict['error'] = 'Book Club name already exists'
        except ValueError:
            return_dict['error'] = 'Failed to validate; Try a different name'

    # Default to assuming GET functionality

    return render(req, 'book_club/create_book_club.html', return_dict)


@login_required
def book_club_home(req, book_club_slug):
    """
    Home page for a given book club
    """

    return_dict = {}

    # Get the book club and reader role
    # TODO - See if we can query for the book club and check publicity OR user having role in one query
    try:
        book_club = BookClub.objects.get(
            slug=book_club_slug,
            disbanded__isnull=True,
        )

        # Ensure that the reader has a role in the club or the club is public
        try:
            return_dict['reader_role'] = book_club.bookclubreaders_set.get(
                reader__id=req.user.id, left__isnull=True
            ).club_role
        except BookClubReaders.DoesNotExist:
            if book_club.publicity != 'PB':
                return redirect('home')
            else:
                return_dict['reader_role'] = None

        return_dict['book_club'] = book_club

    # If the book club doesn't exist, redirect
    except BookClub.DoesNotExist:
        return redirect('home')

    # Get any open membership requests from the DB
    try:
        membership_requested = MembershipRequest.objects.filter(
            reader_id=req.user.id,
            book_club__slug=book_club_slug,
            status__in=[MembershipRequest.RequestStatus.OPEN, MembershipRequest.RequestStatus.VIEWED]
        ).count() > 0

        return_dict['membership_requested'] = membership_requested
    except MembershipRequest.DoesNotExist:
        return_dict['membership_requested'] = False

    # TODO - Strip reader IDs from response
    return render(req, 'book_club/book_club_home.html', return_dict)


@login_required
def book_club_search(req):
    """
    Search page and POST for finding book clubs
    """

    return_dict = {'form': BookClubSearchForm, 'search_submitted': False, 'results': []}

    # Search for book clubs on POST
    if req.method == 'POST':
        return_dict['form'] = BookClubSearchForm(req.POST)
        search_text = req.POST.get('search_text')
        if len(search_text) > 0:
            found_book_clubs = BookClub.objects.filter(
                disbanded__isnull=True,
                name__icontains=search_text,
            ).exclude(publicity='PR')

            return_dict['search_submitted'] = True
            return_dict['results'] = found_book_clubs.all()

    # Default to assuming GET functionality
    return render(req, 'book_club/book_club_search.html', return_dict)


@login_required
def book_club_membership_request(req, book_club_slug):
    """
    Book Club membership request page and POST
    """

    # Get the book club from the DB
    try:
        book_club = BookClub.objects.get(
            ~Q(publicity='PR'),
            slug=book_club_slug,
            disbanded__isnull=True
        )

        # Check to see if the reader is already a member
        try:
            membership = book_club.bookclubreaders_set.get(reader_id=req.user.id)
            if membership:
                return redirect('home')
        except BookClubReaders.DoesNotExist:
            pass

        # Check for an existing request
        existing_request: Optional[MembershipRequest] = None
        try:
            existing_request = MembershipRequest.objects.get(reader_id=req.user.id, book_club__slug=book_club_slug)
        except MembershipRequest.DoesNotExist:
            pass

        # On POST, persist a request
        if req.method == 'POST':
            form = MembershipRequestForm(req.POST)
            membership_request: MembershipRequest = form.save(commit=False)

            # If there's already an existing request, update it
            if existing_request is not None:
                existing_request.message = membership_request.message
                existing_request.status = MembershipRequest.RequestStatus.OPEN
                existing_request.save()

            # Otherwise save a new request
            else:
                membership_request.reader = req.user
                membership_request.book_club = book_club
                membership_request.save()

            # Generate a notification about the request
            notification = Notification(
                source_reader=req.user,
                book_club=book_club,
                type=Notification.NotificationType.MEMBERSHIP_REQUESTED
            )
            notification.save()

            return redirect('book_club:book_club_home', book_club_slug=book_club_slug)

        # Default to assuming GET functionality
        return render(
            req,
            'book_club/book_club_membership_request_form.html',
            {
                'form': MembershipRequestForm,
                'book_club_name': book_club.name,
                'membership_requested': existing_request is not None
            }
        )

    # If the reader is a member of the group already or the group is private, redirect
    except BookClub.DoesNotExist:
        return redirect('book_club:book_club_home', book_club_slug=book_club_slug)


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

            return redirect('book_club:book_club_admin_membership_requests', book_club_slug=book_club_slug)
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

            return redirect('book_club:book_club_admin_membership_requests', book_club_slug=book_club_slug)
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
