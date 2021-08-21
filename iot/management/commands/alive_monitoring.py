from django.core.management.base import BaseCommand
from iot.models import User, DeviceModel, NumberModel, ImageModel
from django.conf import settings

from django.core.mail import send_mail
import requests

import datetime

def mkmess(l):
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
            if not user.alive_monitoring:
                continue
            
            devices = DeviceModel.objects.filter(email=user, monitoring=True, is_active=True).order_by('channel', 'name').select_related()
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
                print('Message send to ' + user.email)
                context = mkmess(dead_device)
                if user.send_message_to_email:
                    from_email = 'EMAIL_ADDRESS'
                    #recipient_list = [user.email]
                    subject = 'Your Device Is Stpping '#メールタイトル
                    user.email_user(subject, context, from_email)
                    #send_mail(subject, context, from_email, recipient_list)

                if user.line_token!='' and user.send_message_to_line:
                    user.line_user(msg=context)

                if user.slack_token!='' and user.slack_channel!='' and user.send_message_to_slack:
                    user.slack_user(msg=context)
                
        print("END Alive Monitoring")
                