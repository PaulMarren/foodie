from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal receiver that automatically creates a Profile whenever a new User is created.
    """
    if created:  # Only execute for newly created Users
        Profile.objects.create(user=instance)  # Create associated Profile


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Signal receiver that ensures the User's Profile is saved whenever the User is saved.
    This handles cases where the User is updated after initial creation.
    """
    instance.profile.save()  # Save the associated Profile