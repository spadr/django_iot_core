from django.db import models
from iot.models.custom_user import User
import uuid


class DeviceModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100)
    data_type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    monitoring = models.BooleanField(default=False)
    interval = models.IntegerField(null=True)
    activity = models.DateTimeField()