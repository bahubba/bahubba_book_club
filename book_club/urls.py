from django.urls import path, include

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
    path('<slug:book_club_slug>/admin/', include('book_club_admin.urls'))
]