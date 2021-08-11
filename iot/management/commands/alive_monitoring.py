from django.core.management.base import BaseCommand
from iot.views.models import DeviceModel, Profile
from django.contrib.auth.models import User
from django.conf import settings

from django.core.mail import send_mail
import requests

import datetime

def mkmess(l,username):
    message = '\nYour device is stopping!\n'
    for dev in l:
        message += '['+dev[0]+'/'+dev[1]+']'+'\n'
        message += '   '+str(dev[2])+'mins before\n'
    return message


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("START Alive Monitoring")
        now_timestamp = int(datetime.datetime.now().timestamp())
        devices = DeviceModel.objects.filter(monitoring=True, is_active=True).select_related()
        users = User.objects.all()
        for user in users:
            profile = Profile.objects.get(user=user)
            if not profile.alive_monitoring:
                continue
            
            devices = DeviceModel.objects.filter(user=user, monitoring=True, is_active=True).order_by('channel', 'name').select_related()
            dead_device = []
            for device in devices:
                latest = device.activity
                timediff = now_timestamp - int(latest.timestamp())
                stopping = device.interval*60<=timediff
                if stopping:
                    dead_device.append([device.channel, device.name, timediff//60])
                    device.is_active=False
                    device.save()
            
            if len(dead_device)!=0:
                if profile.send_message_to_email:
                    from_email = 'EMAIL_ADDRESS'
                    recipient_list = [user.email]
                    subject = 'Your Device Is Stpping '#メールタイトル
                    context = mkmess(dead_device,user.email)
                    print('Email send to ' + user.email)
                    send_mail(subject, context, from_email, recipient_list)

                if profile.line_token!='' and profile.send_message_to_line:
                    ACCESS_TOKEN = profile.line_token
                    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
                    data = {"message": mkmess(dead_device,user.email)}
                    requests.post("https://notify-api.line.me/api/notify",headers=headers,data=data,)
                    print('LINE send to ' + ACCESS_TOKEN)
        print("END Alive Monitoring")
                