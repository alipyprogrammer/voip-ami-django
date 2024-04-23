from rest_framework import generics
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import *
import colorama
from django.views import View
from colorama import Fore
from django.shortcuts import render
from django.db.models import Q
from datetime import datetime , timedelta
import json
import requests
from rest_framework.generics import ( 
    CreateAPIView,
    ListCreateAPIView ,
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from User.permissions import *
from time import sleep
import openpyxl
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from .serializers import QueueLogSerializer


@api_view(['POST'])
def AddQueueLog_5040(request):
    Data = request.data
    user = request.user
    addList = []
    if user.robotVoip : 
        for i in Data:
            createObject = QueueLog(
                    idd  = i['id'],
                    time  = i['time'],
                    callid  = i['callid'],
                    queuename  = i['queuename'],
                    serverid  = i['serverid'],
                    agent  = i['agent'],
                    event  = i['event'],
                    data1  = i['data1'],
                    data2  = i['data2'],
                    data3  = i['data3'],
                    data4  = i['data4'],
                    data5  = i['data5'],
            )
            addList.append(createObject)
        QueueLog.objects.using("5040").bulk_create(addList)
        return Response({
            "status": True,
            "message": "done",
            "data": "done"
        }, status=200)
    else:
        return Response({
            "status": False,
            "message": "failed",
        }, status=403)


@api_view(['GET'])
def LastQueueLog_5040(request):
    last_record = QueueLog.objects.using("5040").latest("id")
    if int(last_record.idd) > 20 : 
        return Response({
                "status": True,
                "message": "done",
                "data": last_record.idd
        }, status=200)
    else:
        return Response({
                "status": False,
                "message": "id < 20",
        }, status=500)


@api_view(['POST'])
def AddQueueLog_hamkadeh(request):
    Data = request.data
    user = request.user
    addList = []
    if user.robotVoip : 
        for i in Data:
            createObject = QueueLoghamkadeh(
                    idd  = i['id'],
                    time  = i['time'],
                    callid  = i['callid'],
                    queuename  = i['queuename'],
                    serverid  = i['serverid'],
                    agent  = i['agent'],
                    event  = i['event'],
                    data1  = i['data1'],
                    data2  = i['data2'],
                    data3  = i['data3'],
                    data4  = i['data4'],
                    data5  = i['data5'],
            )
            addList.append(createObject)
        QueueLoghamkadeh.objects.using("hamkadeh").bulk_create(addList)
        return Response({
            "status": True,
            "message": "done",
            "data": "done"
        }, status=200)
    else:
        return Response({
            "status": False,
            "message": "failed",
        }, status=403)


@api_view(['GET'])
def LastQueueLog_hamkadeh(request):
    last_record = QueueLoghamkadeh.objects.using("hamkadeh").latest("id")
    if int(last_record.idd) > 20 : 
        return Response({
                "status": True,
                "message": "done",
                "data": last_record.idd
        }, status=200)
    else:
        return Response({
                "status": False,
                "message": "id < 20",
        }, status=500)





