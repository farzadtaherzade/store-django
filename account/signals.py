from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import Profile
import os


@receiver(pre_save, sender=Profile)
def delete_old_avatar(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Profile.objects.get(pk=instance.pk)
            # Check if avatar is being changed
            if old_instance.avatar != instance.avatar:
                # Delete old avatar file if it exists
                if old_instance.avatar:
                    if os.path.exists(old_instance.avatar.path):
                        os.remove(old_instance.avatar.path)
        except Profile.DoesNotExist:
            pass
