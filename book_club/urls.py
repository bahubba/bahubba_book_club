from django.urls import path

from . import views

app_name = 'book_club'

urlpatterns = [
    path('', views.book_clubs, name='book_clubs'),
    path('create', views.create_book_club, name='create_book_club'),
    path('<slug:book_club_slug>/', views.book_club_home, name='book_club_home'),
    path('search', views.book_club_search, name='book_club_search'),
    path(
        '<slug:book_club_slug>/request-membership',
        views.book_club_membership_request,
        name='book_club_membership_request'
    ),
    path('<slug:book_club_slug>/admin', views.book_club_admin, name='book_club_admin'),
    path('<slug:book_club_slug>/admin/members', views.book_club_admin_members, name='book_club_admin_members'),
    path('<slug:book_club_slug>/admin/prefs', views.book_club_admin_prefs, name='book_club_admin_prefs'),
    path(
        '<slug:book_club_slug>/admin/members/change-role',
        views.book_club_admin_change_role,
        name='book_club_admin_change_role'
    ),
    path(
        '<slug:book_club_slug>/admin/members/remove',
        views.book_club_admin_remove_reader,
        name='book_club_admin_remove_reader'
    ),
    path(
        '<slug:book_club_slug>/admin/membership-requests',
        views.book_club_admin_membership_requests,
        name='book_club_admin_membership_requests'
    ),
    path(
        '<slug:book_club_slug>/admin/membership-requests/approve',
        views.book_club_admin_approve_new_reader,
        name='book_club_admin_approve_new_reader'
    ),
    path(
        '<slug:book_club_slug>/admin/membership-requests/deny',
        views.book_club_admin_reject_new_reader,
        name='book_club_admin_reject_new_reader'
    ),
    path(
        '<slug:book_club_slug>/admin/disband',
        views.book_club_admin_disband,
        name='book_club_admin_disband'
    ),
]