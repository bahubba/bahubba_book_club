import traceback
from typing import Optional

from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import BookClub, Reader
from .forms import BookClubForm, ReaderCreationForm


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
                # Create and persist the Reader (User)
                reader = Reader.objects.create_user(
                    username=req.POST['username'],
                    email=req.POST['email'],
                    password=req.POST['password1'],
                    given_name=req.POST['given_name'],
                    surname=req.POST['surname'],
                )
                reader.save()
                login(req, reader)
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
            # TODO - See if generating UUID here allows for commit=False
            new_book_club = form.save()
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
def book_club_home(req, book_club_name):
    """
    Home page for a given book club
    """

    # Get the book club from the DB
    book_club: Optional[BookClub]
    try:
        print(BookClub.objects.filter(
            name=book_club_name,
            disbanded__isnull=True,
            readers__id=req.user.id,
            bookclubreaders__left__isnull=True,
        ).query)
        book_club = BookClub.objects.get(
            name=book_club_name,
            disbanded__isnull=True,
            readers__id=req.user.id,
            bookclubreaders__left__isnull=True,
        )
    except BookClub.DoesNotExist:
        book_club = None

    # If the reader isn't a member of the group, redirect
    # TODO - redirect to current page instead of home
    if book_club is None:
        return redirect('home')

    # TODO - Strip reader IDs from response
    return render(req, 'book_club/book_club_home.html', {'book_club': book_club})


@login_required
def book_club_admin(req, book_club_name):
    """
    Base admin page for managing a book club
    """

    # Get the book club from the DB
    book_club = __get_admin_club_or_none(book_club_name, req.user.id)

    # If not an admin, redirect to home
    # TODO - Redirect to current page
    if book_club is None:
        return redirect('home')

    return render(
        req,
        'book_club/book_club_admin.html',
        {'book_club': book_club, 'title': f'Manage {book_club_name} Details', 'section': 'details'},
    )


@login_required
def book_club_admin_members(req, book_club_name):
    """
    Manage membership for book club
    """

    # Get the book club from the DB
    book_club = __get_admin_club_or_none(book_club_name, req.user.id)

    # If not an admin, redirect to home
    # TODO - Redirect to current page
    if book_club is None:
        return redirect('home')

    print('book_club:', book_club.bookclubreaders_set.all)

    return render(
        req,
        'book_club/book_club_admin.html',
        {
            # TODO - filter readers to only those who haven't left
            'book_club': book_club,
            'title': f'Manage {book_club_name} Members',
            'section': 'members',
        },
    )


@login_required
def book_club_admin_prefs(req, book_club_name):
    """
    Manage book club preferences
    """

    # Get the book club from the DB
    book_club = __get_admin_club_or_none(book_club_name, req.user.id)

    # If not an admin, redirect to home
    # TODO - Redirect to current page
    if book_club is None:
        return redirect('home')

    return render(
        req,
        'book_club/book_club_admin.html',
        {
            'book_club': book_club,
            'title': f'Manage {book_club_name} Preferences',
            'section': 'prefs',
        }
    )


@login_required
def book_club_admin_change_role(req, book_club_name):
    pass


@login_required
def book_club_admin_remove_reader(req, book_club_name):
    pass


@login_required
def book_club_admin_disband(req, book_club_name):
    """
    Disband a book club (soft delete)
    """

    # Get the book club from the DB
    # TODO - Only creators should be able to disband groups
    book_club = __get_admin_club_or_none(book_club_name, req.user.id)

    # If not an admin, redirect to home
    # TODO - Redirect to current page
    if book_club is None:
        return redirect('home')

    # Set the book club to disbanded and redirect to home
    book_club.disbanded = timezone.now()
    book_club.save()

    return redirect('home')


def __get_admin_club_or_none(book_club_name, user_id):
    book_club: Optional[BookClub]
    try:
        book_club = BookClub.objects.get(
            name=book_club_name,
            disbanded__isnull=True,
            readers__id=user_id,
            bookclubreaders__club_role='AD',
            bookclubreaders__left__isnull=True,
        )
    except BookClub.DoesNotExist:
        book_club = None

    return book_club
