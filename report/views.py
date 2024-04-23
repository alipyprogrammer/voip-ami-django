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
from rest_framework.generics import get_object_or_404
from .models import *
from .serializer import *
from User.permissions import *
from rest_framework.response import Response
from rest_framework import status




def string_to_list(string):
    try:
        result_list = eval(string)
        if isinstance(result_list, list):
            return result_list
        else:
            raise ValueError("Input is not a valid list string.")
    except Exception as e:
        print("Error:", e)
        return ([])

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAuthorOrReadOnly])
def calculate_report_voip(request , number):
    
    Data=request.data
    idNumber = number 
    report_get=get_object_or_404(Report,id=idNumber)   
    getReport =  ReportSerializer(report_get)   

    

    result=Call_log_report(Data['start'],
                           Data['end'],
                           getReport.data['type'],
                           string_to_list(getReport.data['agent']),
                           string_to_list(getReport.data['queue_log']),
                           getReport.data['company']
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
            "data" :  "NO Report"
        },status=400)


@permission_classes([IsAuthenticated,IsAuthorOrReadOnly])
class DeleteDetailAPIView(APIView):
    def get(self, request, report_id):
        report = get_object_or_404(Report, id=report_id)
        report_serializer = ReportSerializer(instance=report)
        data = report_serializer.data
        return Response({'report': data})

    def delete(self, request, report_id):
        report = get_object_or_404(Report, id=report_id)
        report.delete()
        return Response({'message': "deleted"})



@permission_classes([IsAuthenticated,])
@api_view(['POST','PUT'])
def create_update(request,report_id=None):
    Data=request.data
    User=request.user

    if request.method=="PUT":
        report = get_object_or_404(Report, id=report_id)
        report.name=Data['name']
        report.type=Data['type']
        report.agent=Data['agent']
        report.queue_log=Data['queue_log']
        report.save()
        return Response({'message': "updated"})

    elif request.method=="POST":
        Report.objects.create(name=Data['name'],
                              type=Data['type'],
                              agent=Data['agent'],
                              queue_log=Data['queue_log'],
                              author=User
        )

        return Response({'message': "created"},status=status.HTTP_201_CREATED)

    else:
        return Response({'message': "method not allow"},status=status.HTTP_201_CREATED)
        


@permission_classes([IsAuthenticated])
class ReportList(ListAPIView):
    queryset =Report.objects.all()
    serializer_class =ReportSerializer
    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(author=user)
    






