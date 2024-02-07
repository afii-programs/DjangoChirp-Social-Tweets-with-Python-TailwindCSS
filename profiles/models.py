from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField


# Create your models here.



class Profiles(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    profile_pic = ImageField(upload_to="profile_pics")

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profiles.objects.create(user=instance)

class Skill(models.Model):
    skill = models.CharField(max_length=100, unique=True)
    profiles = models.ManyToManyField(Profiles, related_name='user_skills')

    def __str__(self):
        return self.skill