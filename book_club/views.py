from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from .models import Reader


def register_user(req):
    """
    Reader (User) register view and POST
    """

    # TODO - Probably need custom form...
    return_dict = {'form': UserCreationForm()}

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

                # TODO - Redirect to home page once implemented
                # return redirect('home')
            except IntegrityError:
                return_dict['error'] = 'Username or email has already been taken'

        else:
            return_dict['error'] = 'Passwords do not match'

    # Default to assuming GET functionality; Render the register page
    return render(req, 'book_club/register_user.html', return_dict)


def login_user(req):
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

            # TODO - Redirect to home page once implemented
            # return redirect('home')

    # Default to assuming GET functionality; Render the login page
    return render(req, 'book_club/login_user.html', return_dict)
