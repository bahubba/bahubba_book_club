"""
URL configuration for bahubba_book_club project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from book_club import views

urlpatterns = [
    # Django Administration
    path("admin/", admin.site.urls),

    # Book Club Administration

    # Auth (in Book Clubs)
    path('register/', views.register_reader, name='register'),
    path('login/', views.login_reader, name='login'),
    path('logout/', views.logout_reader, name='logout'),

    # Book Clubs
    path('', views.home, name='home'),
    path('book-clubs/', include('book_club.urls')),

    # Readers

    # Authors

    # Books

    # Notifications
    path('notifications/', include('notifications.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
