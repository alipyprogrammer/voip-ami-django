from django.shortcuts import render
from queuelog.models import *
from .Call_log import *
import pandas as pd
import json
from django.shortcuts import render
from itertools import product
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import  api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,IsAdminUser
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


@api_view(['POST'])
def ReportVoip(request , **kwargs):
    
    Data=request.data

    
    result=Call_log_report(Data['start'],
                           Data['end'],
                           Data['type'],
                           Data['agent'],
                           Data['queue_log']
                           )
   

    
    if  type(result)!=str:  
        voip_report= json.loads(result.to_json(orient='records'))
    
        return Response({
            "status" : True,
            "message" : "done" ,
            "data" : voip_report
        },status=200)
    else:
        return Response({
            "status" : False,
            "message" : "NO Report" ,
            "data" : "NO Report"
        },status=400)



