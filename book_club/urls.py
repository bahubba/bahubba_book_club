from django.urls import path

from . import views

app_name = 'book_club'

urlpatterns = [
    path('', views.book_clubs, name='book_clubs'),
    path('create', views.create_book_club, name='create_book_club'),
    path('<str:book_club_name>/', views.book_club_home, name='book_club_home'),
    path('search', views.book_club_search, name='book_club_search'),
    path('<str:book_club_name>/admin', views.book_club_admin, name='book_club_admin'),
    path('<str:book_club_name>/admin/members', views.book_club_admin_members, name='book_club_admin_members'),
    path('<str:book_club_name>/admin/prefs', views.book_club_admin_prefs, name='book_club_admin_prefs'),
    path(
        '<str:book_club_name>/admin/members/change-role',
        views.book_club_admin_change_role,
        name='book_club_admin_change_role'
    ),
    path(
        '<str:book_club_name>/admin/members/remove',
        views.book_club_admin_remove_reader,
        name='book_club_admin_remove_reader'
    ),
    path(
        '<str:book_club_name>/admin/disband',
        views.book_club_admin_disband,
        name='book_club_admin_disband'
    ),
]