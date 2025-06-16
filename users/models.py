from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_image = CloudinaryField(
        'image',
        blank=True,  # Allow no image
        null=True,   # Allow NULL in database
        default=None # No default image
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"