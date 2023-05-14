from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Reader


class ReaderCreationForm(UserCreationForm):
    class Meta:
        model = Reader
        fields = ("username",)


class ReaderChangeForm(UserChangeForm):
    class Meta:
        model = Reader
        fields = ("username",)
