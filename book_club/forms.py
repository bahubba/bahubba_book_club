from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from .models import BookClub, Reader


class ReaderCreationForm(UserCreationForm):
    class Meta:
        model = Reader
        fields = ("username", "email", "given_name", "surname",)


class ReaderChangeForm(UserChangeForm):
    class Meta:
        model = Reader
        fields = ("username", "email", "given_name", "surname",)


class BookClubForm(ModelForm):
    class Meta:
        model = BookClub
        fields = ['name']
