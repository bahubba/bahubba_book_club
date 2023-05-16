from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm

from .models import BookClub, Reader


class ReaderCreationForm(UserCreationForm):
    class Meta:
        model = Reader
        fields = ("username",)


class ReaderChangeForm(UserChangeForm):
    class Meta:
        model = Reader
        fields = ("username",)


class BookClubForm(ModelForm):
    class Meta:
        model = BookClub
        fields = ['name']
