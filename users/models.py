from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    """
    Extended user profile model that adds additional information to Django's built-in User model.
    Each Profile is linked to a single User via a one-to-one relationship.
    """
    
    # One-to-one relationship with Django's User model - each user has exactly one profile
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE  # Delete profile when user is deleted
    )
    
    # Optional biographical information about the user
    bio = models.TextField(
        max_length=500,  # Limit biography length
        blank=True       # Allow empty bio
    )
    
    # User profile picture hosted on Cloudinary
    profile_image = CloudinaryField(
        'image',         # Cloudinary resource type
        blank=True,      # Form can be submitted without image
        null=True,       # Database can store NULL for no image
        default=None     # No default image
    )

    def __str__(self):
        """String representation of the profile for admin interface and debugging"""
        return f"{self.user.username}'s Profile"
