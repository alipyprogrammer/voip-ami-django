from rest_framework import generics
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
from voip.models import *
import colorama
from django.views import View
from colorama import Fore
from django.shortcuts import render
from django.db.models import Q
from datetime import datetime
from .asteriskAmi import connect_to_ami
import json


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
from voip.serializers import *


class MemberFellowsListView(ListAPIView):
    queryset =MemberFellows.objects.all() 
    serializer_class =MemberFellowsSerializer










@api_view(['POST'])
def ActiveChannelsFellowsViews(request):
    
    data = request.data
    AddItem = data['data']

    channel_layer = get_channel_layer()
 
    print(Fore.BLUE + "============ Active Channels Fellows ==============")
    
    AddItem = data['data']  

    items_to_create = []    
    exitItem = False
    for i in AddItem:
        existing_item = ActiveChannelsFellows.objects.filter(channel=i['channel'])
        if not existing_item.exists():
            exitItem = True
            print(i)
            break

    if exitItem :
        ActiveChannelsFellows.objects.all().delete()   
        print(Fore.BLUE + "deleted")


        nowTime = datetime.now()
        now = nowTime.strftime("%H:%M:%S")

        print(now)
        
        items_to_create = [ActiveChannelsFellows(channel=i['channel'] ,callerID = i['callerID'] ,extension =i['extension'] , duration = i['duration'] ,dateUpdate =now) for i in AddItem]
        ActiveChannelsFellows.objects.bulk_create(items_to_create)

        ActiveChannelsFellowsData = [{'channel': i['channel'] ,'extension': i['extension'], 'callerID' : i['callerID'] ,'duration': i['duration'] , 'dateUpdate': now} for i in AddItem]
        async_to_sync(channel_layer.group_send)(
        "ActiveChannelsFellows_channels",
            {
                "type": "data_ActiveChannelsFellows_channels",
                "data": ActiveChannelsFellowsData,
            },
        )

    nowTime = datetime.now()

    now = nowTime.strftime("%Y-%m-%d %H:%M:%S")

    print(Fore.YELLOW + f"{now}")
    
    print(Fore.BLUE + "done")
    print(Fore.BLUE + "======= Active Channels  End =========")


    return Response('ok')









    

@api_view(['GET'])
def ListLineViews(request):
    try:
        # ami.logoff()
        print("try to connect")
        ami = connect_to_ami()  

        if ami is not None:
            print("Connected to AMI")
            response = ami.command('sip show peers')
            print("type shod")
            channel_data = []
            for line in response.data.split('\n'):
                if line.strip():
                    parts = line.split()
                    name = parts[0]
                    channel_data.append({"name": name})
  #          
            json_data = {"data" : channel_data}
            print("log off Type")
            ami.logoff()
            print("log off ")

            return Response(json_data, status=status.HTTP_200_OK)


    except Exception as e:
        # ami.logoff()
        return Response({'error': 'error to AMI'}, status=status.HTTP_504_GATEWAY_TIMEOUT)





@api_view(['POST'])
def PeersViews(request):
    data = request.data
    AddItem = data['data']

    channel_layer = get_channel_layer()
 
    print(Fore.BLUE + "============ Peers Fellows ==============")
    
    AddItem = data['data']  

    items_to_create = []    
    exitItem = False
    for i in AddItem:
        existing_item = PeersFellows.objects.filter(name=i['name']  , status =i['status'] )
        if not existing_item.exists():
            exitItem = True
            print(i)
            break

    if exitItem :
        PeersFellows.objects.all().delete()   
        print(Fore.BLUE + "deleted")


        nowTime = datetime.now()
        now = nowTime.strftime("%H:%M:%S")
        
        items_to_create = [PeersFellows(name=i['name'] , status =i['status'] ,dateUpdate =now) for i in AddItem]
        PeersFellows.objects.bulk_create(items_to_create)

        PeersData = [{'name': i['name'] ,'status': i['status'] , 'dateUpdate': now} for i in AddItem]
        async_to_sync(channel_layer.group_send)(
        "Peers_channels_Fellows",
            {
                "type": "data_peers_Fellows",
                "data": PeersData,
            },
        )

    
    nowTime = datetime.now()

    now = nowTime.strftime("%Y-%m-%d %H:%M:%S")

    print(Fore.YELLOW + f"{now}")


    print(Fore.BLUE + "done")
    print(Fore.BLUE + "======= End =========")


    return Response('ok')


   



   





    


@api_view(['POST'])
def QueueViews(request):

    data = request.data

    MemberData = data['Members']
    exitMemberData = False

    CallersData = data['Callers']
    exitCallerData = False

    channel_layer = get_channel_layer()

    nowTime = datetime.now()
    now = nowTime.strftime("%H:%M:%S")

  
    print(Fore.BLUE + "============ Queue Fellows ==============")



    if len(CallersData) ==0 :
        caller_data = [{'name': i['code'], 'wait': i['wait'] , 'dateUpdate' : now} for i in CallersData]
        CallersFellows.objects.all().delete()   
        async_to_sync(channel_layer.group_send)(
        "caller_channels_Fellows",
            {
                "type": "data_caller_channels_Fellows",
                "data": caller_data,
            },
        )
        print(Fore.YELLOW + "no caller")


    if len(MemberData) ==0 :
        member_data = [{'number': i['code'], 'status': i['status']} for i in MemberData]
        MemberFellows.objects.all().delete()   
        async_to_sync(channel_layer.group_send)(
        "member_channels_Fellows",
            {
                "type": "data_member_channels_Fellows",
                "data": member_data,
            },
        )
        print(Fore.YELLOW + "no member")
        


    #Member
    for m in MemberData :
        exist_member_item = MemberFellows.objects.filter(number=m['code'] , status =m['status'] )
        if not exist_member_item.exists():
            exitMemberData = True
            print(f"member  : {m}")
            break

    if  exitMemberData:
        MemberFellows.objects.all().delete()   

        print("member deleted")

        member_items_to_create = [MemberFellows(number=i['code'] , status=i['status'] ) for i in MemberData]
        MemberFellows.objects.bulk_create(member_items_to_create)
        member_data = [{'number': i['code'], 'status': i['status']} for i in MemberData]
        async_to_sync(channel_layer.group_send)(
        "member_channels_Fellows",
            {
                "type": "data_member_channels_Fellows",
                "data": member_data,
            },
        )
        print("member_exist_done")





    #Caller

    for c in CallersData :
        exit_Callers_item = CallersFellows.objects.filter(name=c['code'])
        if not exit_Callers_item.exists():
            exitCallerData = True
            print(f"caller : {c}")
            break

    if exitCallerData:
        CallersFellows.objects.all().delete()  
        
        print("caller deleted")

        Caller_items_to_create = [CallersFellows(name=i['code'] , wait=i['wait'] , dateUpdate =now) for i in CallersData]
        CallersFellows.objects.bulk_create(Caller_items_to_create)
        
        caller_data = [{'name': i['code'], 'wait': i['wait'] , 'dateUpdate' : now} for i in CallersData]
        async_to_sync(channel_layer.group_send)(
        "caller_channels_Fellows",
            {
                "type": "data_caller_channels_Fellows",
                "data": caller_data,
            },
        )
        print("caller_exist_done")

    nowTime = datetime.now()

    now = nowTime.strftime("%Y-%m-%d %H:%M:%S")

    print(Fore.YELLOW + f"{now}")

    print(Fore.BLUE + "======= End =========")

    return Response('ok')

