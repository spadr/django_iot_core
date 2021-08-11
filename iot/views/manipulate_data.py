from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import NumberModel, DeviceModel, Profile

import datetime

from django_pandas.io import read_frame

import pandas as pd


@login_required
def consolefunc(request):
    username = request.user.get_username()
    if request.method == "GET":#GETの処理
        return redirect(request.META['HTTP_REFERER'])
    
    if request.method == "POST":#POSTの処理
        device_name = request.POST['name']
        device_channel = request.POST['channel']
        mode = request.POST['mode']
        if mode == 'select':
            query_parameter = '?name=' + device_name + '&channel=' + device_channel
            return redirect(request.META['HTTP_REFERER'] + query_parameter)
        
        if mode == 'download':
            if device_channel =='$all':
                if device_name =='$all':
                    user_db = NumberModel.objects.filter(device__user=request.user).order_by('time').values('time', 'device__channel', 'device__name', 'data')
                    device_db = DeviceModel.objects.filter(user=request.user)
                else:
                    user_db = NumberModel.objects.filter(device__user=request.user, device__name=device_name).order_by('time').select_related().values('time', 'device__channel', 'device__name', 'data')
                    device_db = DeviceModel.objects.filter(user=request.user, name=device_name)
            else:
                if device_name =='$all':
                    user_db = NumberModel.objects.filter(device__user=request.user, device__channel=device_channel).order_by('time').select_related().values('time', 'device__channel', 'device__name', 'data')
                    device_db = DeviceModel.objects.filter(user=request.user, channel=device_channel)
                else:
                    user_db = NumberModel.objects.filter(device__user=request.user, device__name=device_name, device__channel=device_channel).order_by('time').select_related().values('time', 'device__channel', 'device__name', 'data')
                    device_db = DeviceModel.objects.filter(user=request.user, name=device_name, channel=device_channel)
            df = read_frame(user_db)
            now_ts = int(datetime.datetime.now().timestamp())
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=['+ str(now_ts) +']mypage.csv'
            df_i = df.set_index('time')
            df['time'] = df_i.index.tz_convert('Asia/Tokyo').tz_localize(None)
            df = df.rename(columns={'device__channel': 'channel', 'device__name': 'name'})
            df.to_csv(path_or_buf=response,index=True)
            return response
        
        elif mode == 'delete':
            if device_channel =='$all':
                if device_name =='$all':
                    user_db = NumberModel.objects.filter(device__user=request.user).order_by('time')#.values('time', 'device__channel', 'device__name', 'data')
                    device_db = DeviceModel.objects.filter(user=request.user)
                else:
                    user_db = NumberModel.objects.filter(device__user=request.user, device__name=device_name).order_by('time').select_related()#.values('time', 'device__channel', 'device__name', 'data')
                    device_db = DeviceModel.objects.filter(user=request.user, name=device_name)
            else:
                if device_name =='$all':
                    user_db = NumberModel.objects.filter(device__user=request.user, device__channel=device_channel).order_by('time').select_related()#.values('time', 'device__channel', 'device__name', 'data')
                    device_db = DeviceModel.objects.filter(user=request.user, channel=device_channel)
                else:
                    user_db = NumberModel.objects.filter(device__user=request.user, device__name=device_name, device__channel=device_channel).order_by('time').select_related()#.values('time', 'device__channel', 'device__name', 'data')
                    device_db = DeviceModel.objects.filter(user=request.user, name=device_name, channel=device_channel)
            user_db.delete()
            device_db.delete()
            return redirect(request.META['HTTP_REFERER'])
        
        else:
            pass


def wrap_boolean_check(v):
    return v=='on'

@login_required
def profilefunc(request):
    username = request.user.get_username()
    if request.method == "GET":#GETの処理
        return redirect(request.META['HTTP_REFERER'])
    
    if request.method == "POST":#POSTの処理
        try:
            device_alive_monitoring = wrap_boolean_check(request.POST['alive_monitoring'])
        except:
            device_alive_monitoring = False
        
        try:
            device_send_message_to_email = wrap_boolean_check(request.POST['send_message_to_email'])
        except:
            device_send_message_to_email = False
        
        try:
            device_line_token = request.POST['line_token']
        except:
            device_line_token = ''
        
        try:
            device_send_message_to_line = wrap_boolean_check(request.POST['send_message_to_line'])
        except:
            device_send_message_to_line = False
        
        profile = Profile.objects.get(user=request.user)
        profile.alive_monitoring = device_alive_monitoring
        profile.send_message_to_email = device_send_message_to_email
        profile.line_token = device_line_token
        profile.send_message_to_line = device_send_message_to_line
        profile.save()
        return redirect(request.META['HTTP_REFERER'])