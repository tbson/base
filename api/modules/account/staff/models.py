from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

from services.models.timestamped_model import TimeStampedModel


# Create your models here.


class Staff(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    token_context = models.CharField(max_length=256, blank=True, default="")
    token_signature = models.CharField(max_length=128, blank=True, default="")
    token_refresh_limit = models.DateTimeField(null=True, blank=True, default=None)

    email = models.EmailField(max_length=128, unique=True)
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)

    first_name = models.CharField(max_length=128, blank=True, default="")
    last_name = models.CharField(max_length=128, blank=True, default="")

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name}".strip()

    @property
    def display_name(self) -> str:
        return f"{self.email}: {self.full_name}"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super().delete(*args, **kwargs)

    class Meta:
        db_table = "staffs"
        ordering = ["-user"]
