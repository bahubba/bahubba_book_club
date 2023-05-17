from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
                    req.POST['username'], req.POST['email'], req.POST['password1']
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
    reader_clubs = BookClub.objects.filter(readers__id=req.user.id).all()
    return_dict = {'book_clubs': reader_clubs, 'in_clubs': len(reader_clubs) > 0}

    return render(req, 'book_club/home.html', return_dict)


@login_required
def book_clubs(req):
    """
    View with readers' book clubs
    """

    # Pull the groups the reader is a member of
    reader_clubs = BookClub.objects.filter(readers__id=req.user.id).all()
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
            new_book_club.readers.add(req.user)
            new_book_club.save()

            return redirect('book_club:book_clubs')
        except IntegrityError:
            return_dict['error'] = 'Book Club name already exists'
        except ValueError:
            return_dict['error'] = 'Failed to validate'

    return render(req, 'book_club/create_book_club.html', return_dict)


@login_required
def book_club_home(req, book_club_name):
    """
    Home page for a given book club
    """

    # Get the book club from the DB
    book_club = get_object_or_404(BookClub, name=book_club_name)

    # TODO - If the reader isn't a member of the group, redirect
    is_member = next((reader for reader in book_club.readers.all() if reader.id == req.user.id), None)
    if is_member is None:
        pass

    # TODO - Strip reader IDs from response
    return render(req, 'book_club/book_club_home.html', {'book_club': book_club})
