from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.core import serializers
from django.db import transaction

from .models import DeviceModel, NumberModel, ImageModel

import secrets
import datetime
import json

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from .forms import ImageForm

from django.utils import timezone
UTC = datetime.timezone(datetime.timedelta(hours=0), 'UTC')


class DeviceSetApi(APIView):
    def get(self, request):
        now_timestamp = int(datetime.datetime.now().timestamp())
        response = {'time': now_timestamp}
        return Response(response, status=HTTP_200_OK)

    def post(self, request):
        now_timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
                return Response(status=HTTP_401_UNAUTHORIZED)
        
        datas = json.loads(request.body)
        packet = datas['content']
        device_name = packet['name']
        device_channel = packet['channel']
        device_type = packet['type']
        device_min = int(packet['interval'])
        device_status = bool(packet['monitoring'])
        
        try:
            device = DeviceModel.objects.filter(user=request.user, channel=device_channel, name=device_name).order_by('activity').reverse().select_related()[0]
            #device = DeviceModel.objects.get(user=request.user, channel=device_channel, name=device_name)
        except:
            device = DeviceModel.objects.create(user=request.user,
                                                name=device_name,
                                                channel=device_channel,
                                                data_type=device_type,
                                                is_active=True,
                                                monitoring=device_status,
                                                interval=device_min,
                                                activity=timezone.localtime(datetime.datetime.fromtimestamp(now_timestamp, UTC))
                                                )
        else:
            #device.activity=timezone.localtime(datetime.datetime.fromtimestamp(now_timestamp, UTC))
            device.data_type=device_type
            device.is_active=True
            device.monitoring=device_status
            device.interval=device_min
            device.save()
        
        response = {'time': now_timestamp, 'device_token': device.id}
        return Response(response, status=HTTP_201_CREATED)#正常終了のレスポンス


class DataReceiveApi(APIView):
    def get(self, request):
        now_timestamp = int(datetime.datetime.now().timestamp())
        response = {'time': now_timestamp}
        return Response(response, status=HTTP_200_OK)

    def post(self, request):
        now_timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
                return Response(status=HTTP_401_UNAUTHORIZED)
        
        datas = json.loads(request.body)
        content = datas['content']
        for packet in content:
            device_token = packet['device_token']
            device_time = int(packet['time'])
            device_data = packet['data']
            
            device = DeviceModel.objects.get(user=request.user, id=device_token)
            device.activity = timezone.localtime(datetime.datetime.fromtimestamp(now_timestamp, UTC))
            #if device.is_active == False:
            #send line massege
            device.is_active = True
            device.save()

            #登録処理
            data_type=device.data_type
            if data_type == 'number':
                NumberModel.objects.create(device=device,
                                           time=timezone.localtime(datetime.datetime.fromtimestamp(device_time, UTC)),
                                           data=float(device_data)
                                        )
            
            elif data_type == 'boolean':
                pass
            
            elif data_type == 'string':
                pass
            
            elif data_type == 'array':
                pass
            
            else:
                pass
        
        
        response = {'time': now_timestamp}
        return Response(response, status=HTTP_201_CREATED)#正常終了のレスポンス



class DataSendApi(APIView):
    def get(self, request):
        now_timestamp = int(datetime.datetime.now().timestamp())
        response = {'time': now_timestamp}
        return Response(response, status=HTTP_200_OK)
    
    def post(self, request):
        if not request.user.is_authenticated:
                return Response(status=HTTP_401_UNAUTHORIZED)
        
        datas = json.loads(request.body)
        try:
            device_token = datas['device_token']
            data_lengh = int(datas['lengh']) + 1
            queryset = NumberModel.objects.filter(device__user=request.user, device__id=device_token).order_by('time').reverse().select_related()[:data_lengh]
            res_query = serializers.serialize('json', queryset)
        except:
            return Response(status=HTTP_404_NOT_FOUND)#該当データ無しのレスポンス
        else:
            return HttpResponse(res_query, content_type="text/json-comment-filtered")#正常終了のレスポンス


@login_required
@transaction.atomic
def browserpostfunc(request):
    now_timestamp = int(datetime.datetime.now().timestamp())
    if request.method == "GET":#GETの処理
        return HttpResponse()
    
    if request.method == "POST":#POSTの処理
        device_name = request.POST['name']
        device_channel = request.POST['channel']
        device_value = request.POST['data']
        try:
            device = DeviceModel.objects.get(user=request.user, channel=device_channel, name=device_name)
        except:
            device = DeviceModel.objects.create(user=request.user,
                                                name=device_name,
                                                channel=device_channel,
                                                data_type='number',
                                                is_active=True,
                                                monitoring=False,
                                                #interval=null,
                                                activity=timezone.localtime(datetime.datetime.fromtimestamp(now_timestamp, UTC))
                                                )
        #登録処理
        NumberModel.objects.create(device=device,
                                   time=timezone.localtime(datetime.datetime.fromtimestamp(now_timestamp, UTC)),
                                   data=float(device_value)
                                   )
        
        return redirect(request.META['HTTP_REFERER'])


class ImageReceiveApi(APIView):
    def get(self, request):
        now_timestamp = int(datetime.datetime.now().timestamp())
        response = {'time': now_timestamp}
        return Response(response, status=HTTP_200_OK)

    def post(self, request):
        now_timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
                return Response(status=HTTP_401_UNAUTHORIZED)
        
        img = ImageForm(request.POST, request.FILES)
        if img.is_valid():
            img.save()
        else:
            return Response(status=HTTP_404_NOT_FOUND)
        
        response = {'time': now_timestamp}
        return Response(response, status=HTTP_201_CREATED)#正常終了のレスポンス