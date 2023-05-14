import datetime
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# TODO - Create custom user manager
# TODO - Customize authorization (groups, roles in groups) - May not need to override Django auth for more high-level app functions
# TODO - Finish adding other DB entities


# Readers (Book Club Members) - THESE ARE THE USERS
class Reader(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, null=False
    )
    username = models.CharField(max_length=50, unique=True, null=False)
    is_staff = models.BooleanField(default=False)
    given_name = models.CharField(max_length=50, null=False)
    middle_name = models.CharField(max_length=100, null=True)
    surname = models.CharField(max_length=50, null=False)
    suffix = models.CharField(max_length=15, null=True)
    title = models.CharField(max_length=15, null=True)
    email = models.EmailField(unique=True, null=False)
    joined = models.DateTimeField(default=timezone.now)
    left = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = [
        'email',
        'given_name',
        'surname',
    ]

    def __str__(self):
        return self.username


# Authors
class Author(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, null=False
    )
    given_name = models.CharField(max_length=50, null=True)
    middle_name = models.CharField(max_length=100, null=True)
    surname = models.CharField(max_length=50, null=False)
    suffix = models.CharField(max_length=15, null=True)
    title = models.CharField(max_length=15, null=True)
    display_name = models.CharField(max_length=300, null=False)
    birth_year = models.SmallIntegerField(
        null=True, validators=[MaxValueValidator(datetime.date.today().year)]
    )
    birth_month = models.SmallIntegerField(
        null=True, validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    birth_day = models.SmallIntegerField(
        null=True, validators=[MinValueValidator(1), MaxValueValidator(31)]
    )
    death_year = models.SmallIntegerField(
        null=True, validators=[MaxValueValidator(datetime.date.today().year)]
    )
    death_month = models.SmallIntegerField(
        null=True, validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    death_day = models.SmallIntegerField(
        null=True, validators=[MinValueValidator(1), MaxValueValidator(31)]
    )
    pseudonym_for = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.display_name


# Genres
class Genre(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, null=False
    )
    genre: models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.genre


# Books
class Book(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, null=False
    )
    title = models.CharField(max_length=200, null=False)
    published_year = models.SmallIntegerField(
        null=True, validators=[MaxValueValidator(datetime.date.today().year)]
    )
    published_month = models.SmallIntegerField(
        null=True, validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    published_day = models.SmallIntegerField(
        null=True, validators=[MinValueValidator(1), MaxValueValidator(31)]
    )
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING, null=False)
    genres = models.ManyToManyField(Genre)

    class Meta:
        unique_together = (
            'title',
            'author',
        )

    def __str__(self):
        return f'{self.title} - {self.author.display_name}'
