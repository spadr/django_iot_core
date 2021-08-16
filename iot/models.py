from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

import os
import uuid

def get_photo_upload_path(self, filename):
    root_path = "user/photos"
    user_path = root_path + "/" + self.device.user.username + "/" + self.device.channel + "/" + self.device.name
    user_dir_path = settings.MEDIA_ROOT + "/" + user_path
    if not os.path.exists(user_dir_path):
        os.makedirs(user_dir_path)
    return user_path + "/" + filename


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alive_monitoring = models.BooleanField(default=False)
    send_message_to_email = models.BooleanField(default=False)
    line_token = models.CharField(max_length=100, blank=True, null=True)
    send_message_to_line = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class DeviceModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    channel = models.CharField(max_length=100)
    data_type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    monitoring = models.BooleanField(default=False)
    interval = models.IntegerField(null=True)
    activity = models.DateTimeField()



class NumberModel(models.Model):
    device = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
    time = models.DateTimeField()
    data = models.FloatField(null=True)



class ImageModel(models.Model):
    device = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField('Photo', upload_to=get_photo_upload_path)

@receiver(post_delete, sender=ImageModel)
def delete_file(sender, instance, **kwargs):
    instance.image.delete(False)