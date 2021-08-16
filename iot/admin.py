from django.contrib import admin

from .models import DeviceModel, NumberModel, ImageModel

# Register your models here.

admin.site.register(DeviceModel)
admin.site.register(NumberModel)
admin.site.register(ImageModel)
