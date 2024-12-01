from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_photo = CloudinaryField('profile_photos', blank=True, null=True)  # Update to use Cloudinary
    background_photo = CloudinaryField('background_photos', blank=True, null=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.full_name or self.username 


class LoginActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="login_activities")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)  # Stores device/browser info
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.timestamp}"