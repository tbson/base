from django.db import models
from django.conf import settings

from service.framework.model.timestamped_model import TimeStampedModel


# Create your models here.


class Staff(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @property
    def full_name(self) -> str:
        return self.user.full_name

    @property
    def email(self) -> str:
        return self.user.email

    @property
    def phone_number(self) -> str:
        return self.user.phone_number

    def __str__(self):
        return self.user.email

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super().delete(*args, **kwargs)

    class Meta:
        db_table = "staffs"
        ordering = ["-user"]
