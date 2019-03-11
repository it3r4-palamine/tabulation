from django.db import models
from django.utils import timezone
import uuid


class CommonModel(models.Model):

    uuid         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code         = models.CharField(max_length=100, blank=True, null=True)
    name         = models.CharField(max_length=250, blank=False, null=False)
    description  = models.CharField(max_length=250, blank=True, null=True)
    company      = models.ForeignKey("Company", blank=True, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now, blank=True, null=True)
    date_edited  = models.DateTimeField(default=timezone.now, blank=True, null=True)
    is_global    = models.BooleanField(default=False)
    is_deleted   = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def get_code(self):
        return self.code if self.code else None