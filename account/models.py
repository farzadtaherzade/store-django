from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.user.first_name + self.user.last_name


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance
        )


class Address(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="addresses")
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    pelak = models.IntegerField()

    def __str__(self):
        return f"{self.profile.user.username} - {self.address}"
