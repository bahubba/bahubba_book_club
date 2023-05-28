from django.urls import path

from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notifications_home, name='notifications'),
    path('<str:notification_id>/toggle-viewed', views.toggle_viewed, name='toggle_viewed'),
    path('link', views.link, name='link'),
]