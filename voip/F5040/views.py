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





class Member5040ListView(ListAPIView):
    queryset =Member5040.objects.all() 
    serializer_class =Member5040Serializer








@api_view(['POST'])
def ActiveChannels5040Views(request):
    
    data = request.data
    AddItem = data['data']

    channel_layer = get_channel_layer()
 
    print(Fore.BLUE + "============ Active Channels 5040 ==============")
    
    AddItem = data['data']  

    items_to_create = []    
    exitItem = False
    for i in AddItem:
        existing_item = ActiveChannels5040.objects.filter(channel=i['channel'])
        if not existing_item.exists():
            exitItem = True
            print(i)
            break

    if exitItem :
        ActiveChannels5040.objects.all().delete()   
        print(Fore.BLUE + "deleted")


        nowTime = datetime.now()
        now = nowTime.strftime("%H:%M:%S")

        print(now)
        
        items_to_create = [ActiveChannels5040(channel=i['channel'] ,callerID = i['callerID'] ,extension =i['extension'] , duration = i['duration'] ,dateUpdate =now) for i in AddItem]
        ActiveChannels5040.objects.bulk_create(items_to_create)

        ActiveChannels5040Data = [{'channel': i['channel'] ,'extension': i['extension'], 'callerID' : i['callerID'] ,'duration': i['duration'] , 'dateUpdate': now} for i in AddItem]
        async_to_sync(channel_layer.group_send)(
        "ActiveChannels5040_channels",
            {
                "type": "data_ActiveChannels5040_channels",
                "data": ActiveChannels5040Data,
            },
        )

    
    
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
 
    print(Fore.BLUE + "============ Peers 5040 ==============")
    
    AddItem = data['data']  

    items_to_create = []    
    exitItem = False
    for i in AddItem:
        existing_item = Peers5040.objects.filter(name=i['name'] , status =i['status'] )
        if not existing_item.exists():
            exitItem = True
            print(i)
            break

    if exitItem :
        Peers5040.objects.all().delete()   
        print(Fore.BLUE + "deleted")


        nowTime = datetime.now()
        now = nowTime.strftime("%H:%M:%S")
        
        items_to_create = [Peers5040(name=i['name'] , status =i['status'] ,dateUpdate =now) for i in AddItem]
        Peers5040.objects.bulk_create(items_to_create)

        PeersData = [{'name': i['name'] ,'status': i['status'] , 'dateUpdate': now} for i in AddItem]
        async_to_sync(channel_layer.group_send)(
        "Peers_channels_5040",
            {
                "type": "data_peers_5040",
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

  
    print(Fore.BLUE + "============ Queue 5040 ==============")



    if len(CallersData) ==0 :
        caller_data = [{'name': i['code'], 'wait': i['wait'] , 'dateUpdate' : now} for i in CallersData]
        Callers5040.objects.all().delete()   
        async_to_sync(channel_layer.group_send)(
        "caller_channels_5040",
            {
                "type": "data_caller_channels_5040",
                "data": caller_data,
            },
        )
        print(Fore.YELLOW + "no caller")
        
    if len(MemberData) ==0 :
        member_data = [{'number': i['code'], 'status': i['status']} for i in MemberData]
        Member5040.objects.all().delete()   
        async_to_sync(channel_layer.group_send)(
        "member_channels_5040",
            {
                "type": "data_member_channels_5040",
                "data": member_data,
            },
        )
        print(Fore.YELLOW + "no caller")

    #Member
    for m in MemberData :
        exist_member_item = Member5040.objects.filter(number=m['code'] , status =m['status'] )
        if not exist_member_item.exists():
            exitMemberData = True
            print(f"member  : {m}")
            break

    if  exitMemberData:
        Member5040.objects.all().delete()   

        print("member deleted")

        member_items_to_create = [Member5040(number=i['code'] , status=i['status'] ) for i in MemberData]
        Member5040.objects.bulk_create(member_items_to_create)
        member_data = [{'number': i['code'], 'status': i['status']} for i in MemberData]
        async_to_sync(channel_layer.group_send)(
        "member_channels_5040",
            {
                "type": "data_member_channels_5040",
                "data": member_data,
            },
        )
        print("member_exist_done")





    #Caller

    for c in CallersData :
        exit_Callers_item = Callers5040.objects.filter(name=c['code'])
        if not exit_Callers_item.exists():
            exitCallerData = True
            print(f"caller : {c}")
            break

    if exitCallerData:
        Callers5040.objects.all().delete()  
        
        print("caller deleted")

        Caller_items_to_create = [Callers5040(name=i['code'] , wait=i['wait'] , dateUpdate =now) for i in CallersData]
        Callers5040.objects.bulk_create(Caller_items_to_create)
        
        caller_data = [{'name': i['code'], 'wait': i['wait'] , 'dateUpdate' : now} for i in CallersData]
        async_to_sync(channel_layer.group_send)(
        "caller_channels_5040",
            {
                "type": "data_caller_channels_5040",
                "data": caller_data,
            },
        )
        print("caller_exist_done")
    nowTime = datetime.now()

    now = nowTime.strftime("%Y-%m-%d %H:%M:%S")

    print(Fore.YELLOW + f"{now}")

    
    print(Fore.BLUE + "======= End =========")

    return Response('ok')

