from django.db.models.signals import post_save
from django.dispatch import receiver

from authapp.models import CustomUser, CustomUserDetails


@receiver(post_save, sender=CustomUser)
def sync_user_details(sender, instance, created, **kwargs):
    if created:
        # Create a CustomUserDetails instance for the new user
        CustomUserDetails.objects.create(user=instance, full_name=f"{instance.first_name} {instance.last_name}".strip())
    else:
        # Update full_name in CustomUserDetails if exists
        try:
            details = instance.details  # assuming related_name='details'
            details.full_name = f"{instance.first_name} {instance.last_name}".strip()
            details.save()
        except CustomUserDetails.DoesNotExist:
            # If no related details exist, optionally create one
            CustomUserDetails.objects.create(user=instance,
                                             full_name=f"{instance.first_name} {instance.last_name}".strip())
