from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import random
import string

User = get_user_model()

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    
    def generate_otp(self):
        """Generate a 6-digit OTP."""
        return ''.join(random.choices(string.digits, k=6))
    
    def is_expired(self):
        """Check if the OTP has expired."""
        return timezone.now() > self.expired_at

    def __str__(self):
        return f"OTP for {self.user.email} valid until {self.expired_at}"

