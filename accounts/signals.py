# accounts/signals.py
from django.contrib.auth.signals import user_logged_in
from django.utils.timezone import now
from django.dispatch import receiver
from .models import LoginActivity


@receiver(user_logged_in)
def log_login_activity(sender, request, user, **kwargs):
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    print(f"Logging login activity for {user.email} - IP: {ip_address}, User Agent: {user_agent}")
    LoginActivity.objects.create(user=user, ip_address=ip_address, user_agent=user_agent)

def get_client_ip(request):
    """Retrieve IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

user_logged_in.connect(log_login_activity)
