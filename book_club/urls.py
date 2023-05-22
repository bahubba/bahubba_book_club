from django.urls import path

from . import views

app_name = 'book_club'

urlpatterns = [
    path('', views.book_clubs, name='book_clubs'),
    path('create', views.create_book_club, name='create_book_club'),
    path('<str:book_club_name>/', views.book_club_home, name='book_club_home'),
    path('<str:book_club_name>/admin', views.book_club_admin, name='book_club_admin'),
]