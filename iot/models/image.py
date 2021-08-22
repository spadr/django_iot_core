from django.db import models
from iot.models.device import DeviceModel
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import os
import uuid

def get_photo_upload_path(self, filename):
    root_path = "user/photos"
    user_path = root_path + "/" + self.device.email + "/" + self.device.channel + "/" + self.device.name
    user_dir_path = settings.MEDIA_ROOT + "/" + user_path
    if not os.path.exists(user_dir_path):
        os.makedirs(user_dir_path)
    return user_path + "/" + filename


class ImageModel(models.Model):
    device = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField('Photo', upload_to=get_photo_upload_path)

@receiver(post_delete, sender=ImageModel)
def delete_file(sender, instance, **kwargs):
    instance.image.delete(False)