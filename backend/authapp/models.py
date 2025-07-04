from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Enforce unique email
    is_verified = models.BooleanField(default=False)  # For email verification

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Change the related_name to avoid conflict
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",  # Change the related_name to avoid conflict
        blank=True,
    )

    def __str__(self):
        return self.username


class CustomUserDetails(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='details')
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        unique=True,
        blank=True,
        null=True
    )
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Auto-fill `full_name` from `first_name` and `last_name` of `CustomUser`
        if self.user.first_name or self.user.last_name:
            self.full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Details of {self.user.username}"