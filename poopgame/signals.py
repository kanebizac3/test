from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UnpPoint

@receiver(post_save, sender=User)
def create_unppoint(sender, instance, created, **kwargs):
    if created:
        UnpPoint.objects.create(user=instance)
