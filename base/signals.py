from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=get_user_model())
def hash_password(sender, instance, created, **kwargs):
    if created:
        instance.set_password(instance.password)
        instance.save()