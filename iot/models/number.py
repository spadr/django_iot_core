from django.db import models
from iot.models.device import DeviceModel
import uuid

class NumberModel(models.Model):
    device = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = models.DateTimeField()
    data = models.FloatField(null=True)