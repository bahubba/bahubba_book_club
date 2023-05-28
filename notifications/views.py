from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def notifications_home(req):
    """
    Page to view notifications
    """

    return render(req, 'notifications/notifications_home.html')