from django.urls import path

from . import views

app_name = 'book_club'

urlpatterns = [
    path('', views.book_clubs, name='book_clubs')
]