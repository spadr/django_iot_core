from django import forms

from iot.models import User, DeviceModel, NumberModel, ImageModel

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('alive_monitoring', 
                  'send_message_to_email', 
                  'line_token', 
                  'send_message_to_line',
                  'slack_token',
                  'slack_channel',
                  'send_message_to_slack',)


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ('device', 'image')