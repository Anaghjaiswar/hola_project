from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    background_photo = models.ImageField(upload_to='background_photos/', blank=True, null=True)
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
