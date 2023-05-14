"""
URL configuration for bahubba_book_club project.
"""
from django.contrib import admin
from django.urls import path

from book_club import views

urlpatterns = [
    # Django Administration
    path("admin/", admin.site.urls),
    # Book Club Administration
    # Book Clubs
    path('signup/', views.signup_user, name='signup'),
    path('login/', views.login_user, name='login'),
    # Readers
    # Authors
    # Books
]
