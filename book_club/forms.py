from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import CharField, Form, ModelForm, Textarea, TextInput

from .models import BookClub, Reader


class ReaderCreationForm(UserCreationForm):
    class Meta:
        model = Reader
        fields = ["username", "email", "given_name", "surname", ]


class ReaderChangeForm(UserChangeForm):
    class Meta:
        model = Reader
        fields = ["username", "email", "given_name", "surname", ]


class BookClubForm(ModelForm):
    class Meta:
        model = BookClub
        fields = ['name', 'image', 'description', 'publicity', ]


class BookClubSearchForm(Form):
    search_text = CharField(
        widget=TextInput(attrs={
            'id': 'search-text',
            'class': 'form-control',
            'aria-describedby': 'Book Club Search',
            'placeholder': 'Search for Book Club'
        }),
        required=True
    )


class MembershipRequestForm(Form):
    message = CharField(
        label='Request Message',
        widget=Textarea(attrs={
            'id': 'request-message',
            'class': 'form-control',
            'aria-describedby': 'Membership request message',
            'placeholder': 'Write a brief introduction here or tell the group why you would like to join'
        }),
        required=True
    )

