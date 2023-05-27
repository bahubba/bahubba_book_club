from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import CharField, Form, ModelForm, Textarea, TextInput, HiddenInput

from .models import BookClub, Reader, MembershipRequest


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


class MembershipRequestForm(ModelForm):
    def __init__(self, *args):
        super().__init__(*args)

        self.fields['message'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['rows'] = 2
        self.fields['message'].widget.attrs['aria-describedby'] = 'Membership request message',
        self.fields['message'].widget.attrs['placeholder'] = 'Write a brief introduction here or tell the group why you would like to join'

    class Meta:
        model = MembershipRequest
        fields = ['message', ]
        widgets = {'message': Textarea}
