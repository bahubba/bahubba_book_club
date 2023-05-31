from django.urls import path

from . import views

app_name = 'book_club_admin'

urlpatterns = [
    path('', views.book_club_admin, name='book_club_admin'),
    path('members', views.book_club_admin_members, name='book_club_admin_members'),
    path('prefs', views.book_club_admin_prefs, name='book_club_admin_prefs'),
    path(
        'change-role',
        views.book_club_admin_change_role,
        name='book_club_admin_change_role'
    ),
    path(
        'members/remove',
        views.book_club_admin_remove_reader,
        name='book_club_admin_remove_reader'
    ),
    path(
        'membership-requests',
        views.book_club_admin_membership_requests,
        name='book_club_admin_membership_requests'
    ),
    path(
        'membership-requests/approve',
        views.book_club_admin_approve_new_reader,
        name='book_club_admin_approve_new_reader'
    ),
    path(
        'membership-requests/deny',
        views.book_club_admin_reject_new_reader,
        name='book_club_admin_reject_new_reader'
    ),
    path(
        'disband',
        views.book_club_admin_disband,
        name='book_club_admin_disband'
    ),
]