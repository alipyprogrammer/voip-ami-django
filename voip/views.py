from rest_framework import generics
from .models import ActiveChannels
from .serializers import *
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import *
import colorama
from django.views import View
from colorama import Fore
from django.shortcuts import render
from django.db.models import Q
from datetime import datetime
from .asteriskAmi import connect_to_ami
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


class ForwardListView(ListAPIView):
    queryset =Forward.objects.all() 
    serializer_class =ForwardSerializer
  # permission_classes=(ForwardPermission ,)

class MemberListView(ListAPIView):
    queryset =Member.objects.all() 
    serializer_class =MemberSerializer



@api_view(['POST'])
def ForwardInExcelView(request):
    data= request.data
    user= request.user


    excel = data['excel']
    company = data['company']
    Add   = data['Add']



    UserCheck = False
    url = ""

    if company == "5040":
        if user.isForward5040:
            url = "https://46.32.25.74:22430/Api/ForwardToMobile.php"
            UserCheck = True
        else:
            return Response({"hamkadeh : شما دستری ندارید"}, status=status.HTTP_403_FORBIDDEN)

    if company == "sale-hamkadeh":
        if user.isForwardSaleHamkadeh:
            url = "https://46.32.25.74:22425/Api/ForwardToMobile.php"
            UserCheck = True
        else:
            return Response({"hamkadeh : شما دستری ندارید"}, status=status.HTTP_403_FORBIDDEN)

    if company == "hamkadeh":
        
        if user.isForwardHamkadeh:
            url= "https://46.32.25.74:22428/Api/ForwardToMobile.php"
            UserCheck = True
        else:
            return Response({"hamkadeh : شما دستری ندارید"}, status=status.HTTP_403_FORBIDDEN)

    if UserCheck:
        df = pd.read_excel(excel)

        if "code" not in df.columns:
            return Response({"فرمت اشتباه می باشد"}, status=status.HTTP_400_BAD_REQUEST)
        
        elif "phone" not in df.columns:
            return Response({"فرمت اشتباه می باشد"}, status=status.HTTP_400_BAD_REQUEST)
        
        df = df[["code", "phone"]]

        if Add == False:
            DataCheckAll = Forward.objects.filter(
                company=company
            )
            for forward in DataCheckAll:
                forward.flag = "0"
                forward.save()

        
        for i in range(len(df)):
            actions ="insert"
            phone = f"0{df.loc[i, 'phone']}"
            code  = f"{df.loc[i, 'code']}"
            
            DataCheck = Forward.objects.filter(
                extension =code ,
                company=company
            ).exists()

            if DataCheck :
                CheckIdSend =requests.get(f"{url}?action=get" , verify=False)
            
                if CheckIdSend.status_code == 200 :
                    listFix  = json.loads(CheckIdSend.text) 
                    for item in listFix:
                        if item["Extension"] == code:
                            idItem = item["id"]
                            pathUpdate = f"{url}?action=update&id={idItem}&MobileNumber={phone}&Extension={code}&Flag=1"
                            SendUpdate = requests.get(pathUpdate , verify=False)
                            if SendUpdate.status_code == 200 :
                                GetIdInModel = Forward.objects.get(extension =code ,company=company)
                                print(GetIdInModel.id)
                                GetIdInModel.actions = "update"
                                GetIdInModel.mobileForward = phone
                                GetIdInModel.extension = code
                                GetIdInModel.flag = "1"
                                GetIdInModel.save()
            else :
                pathAdd = f"{url}?action={actions}&MobileNumber={phone}&Extension={code}&Flag=1"
                Send  = requests.get(pathAdd , verify=False)
                if Send.status_code == 200 :
                    Forward.objects.create(
                        actions = actions,
                        mobileForward = phone,
                        extension = code,
                        flag = '1',
                        company = company,
                    )






    return Response({"done "}, status=status.HTTP_200_OK)














@api_view(['POST'])
def ForwardView(request):
    data= request.data
    user= request.user
    
    actions = data['actions']
    
    mobileForward = data['mobileForward']
    
    extension = data['extension']
    
    flag = data['flag']
    
    company = data['company']
    
    url = ""


    UserCheck = False

    if company == "5040":
        if user.isForward5040:
            url = "https://46.32.25.74:22430/Api/ForwardToMobile.php"
            UserCheck = True
        else:
            return Response({"hamkadeh : شما دستری ندارید"}, status=status.HTTP_403_FORBIDDEN)

    if company == "sale-hamkadeh":
        if user.isForwardSaleHamkadeh:
            url = "https://46.32.25.74:22425/Api/ForwardToMobile.php"
            UserCheck = True
        else:
            return Response({"hamkadeh : شما دستری ندارید"}, status=status.HTTP_403_FORBIDDEN)

    if company == "hamkadeh":
        
        if user.isForwardHamkadeh:
            url= "https://46.32.25.74:22428/Api/ForwardToMobile.php"
            UserCheck = True
        else:
            return Response({"hamkadeh : شما دستری ندارید"}, status=status.HTTP_403_FORBIDDEN)

    DataCheck = Forward.objects.filter(extension =extension ,company=company).exists()
    
    if UserCheck:
        if DataCheck :
            CheckIdSend =requests.get(f"{url}?action=get" , verify=False)
            if CheckIdSend.status_code == 200 :
                listFix  = json.loads(CheckIdSend.text) 
                for item in listFix:
                    if item["Extension"] == extension:
                        idItem = item["id"]
                        pathUpdate = f"{url}?action=update&id={idItem}&MobileNumber={mobileForward}&Extension={extension}&Flag={flag}"
                        SendUpdate = requests.get(pathUpdate , verify=False)
                        if SendUpdate.status_code == 200 :
                            GetIdInModel = Forward.objects.get(extension =extension ,company=company)
                            print(GetIdInModel.id)
                            GetIdInModel.actions = "update"
                            GetIdInModel.mobileForward = mobileForward
                            GetIdInModel.extension = extension
                            GetIdInModel.flag = flag
                            GetIdInModel.save()
                            return Response({f"{company} : success"}, status=status.HTTP_200_OK)
                        else :
                            return Response({f"{company} : error"}, status=status.HTTP_408_REQUEST_TIMEOUT)
        else :
            pathAdd = f"{url}?action={actions}&MobileNumber={mobileForward}&Extension={extension}&Flag={flag}"
            Send  = requests.get(pathAdd , verify=False)
            if Send.status_code == 200 :
                Forward.objects.create(
                    actions = actions,
                    mobileForward = mobileForward,
                    extension = extension,
                    flag = flag,
                    company = company,
                )
                return Response({f"{company} : success"}, status=status.HTTP_200_OK)
            else:
                return Response({f"{company} : success"}, status=status.HTTP_408_REQUEST_TIMEOUT)
        


    
    
    



@api_view(['POST'])
@permission_classes([ListeningHamkadehPermission])
def ListeningHamkadehView(request):
    data = request.data

    channel = data['channel']

    Extension = data['Extension']
    
    Company = data['Company']

 
    hamkadeh = requests.post(f"https://46.32.25.74:22428/Api/ChanSpyApi.php?channel={channel}&Extension={Extension}" , verify=False) 
    if hamkadeh.status_code == 200:
        return Response({f"hamkadeh : {hamkadeh}"}, status=status.HTTP_200_OK)
    else:
        return Response({"hamkadeh : error"}, status=status.HTTP_504_GATEWAY_TIMEOUT)

@api_view(['POST'])
@permission_classes([Listening5040Permission])
def Listening5040(request):
    data = request.data

    channel = data['channel']

    Extension = data['Extension']
    
    Company = data['Company']

    F5040    = requests.post(f"https://46.32.25.74:22430/Api/ChanSpyApi.php?channel={channel}&Extension={Extension}" , verify=False)  
    if F5040.status_code == 200:
        return Response({f"5040 : {F5040} "}, status=status.HTTP_200_OK)
    else:
        return Response({"5040 : error   "}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        


@api_view(['POST'])
@permission_classes([Listening5040Permission])
def ListeningSaleHamkadeh(request):
    data = request.data

    channel = data['channel']

    Extension = data['Extension']
    
    Company = data['Company']

    SaleHamkadeh    = requests.post(f"https://46.32.25.74:22425/Api/ChanSpyApi.php?channel={channel}&Extension={Extension}" , verify=False)  
    message = json.loads(f"{SaleHamkadeh.text}")
    if SaleHamkadeh.status_code == 200:
        return Response({f"sale-hamkadeh : {message} "}, status=status.HTTP_200_OK)
    else:
        return Response({"sale-hamkadeh : error   "}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        





@api_view(['POST'])
def PeerToInExcelLine(request):
    
    data = request.data

    user = request.user



    excel = data['excel']
    company = data['company']
   


    UserCheck = False
    url = ""

    if company == "5040":
        if user.isAddToLine5040:
            url = "https://46.32.25.74:22430/Api/QueueApi.php"
            UserCheck = True
        else:
            return Response({"hamkadeh : شما دستری ندارید"}, status=status.HTTP_403_FORBIDDEN)

    if company == "sale-hamkadeh":
        if user.isAddToLineSaleHamkadeh:
            url = "https://46.32.25.74:22425/Api/QueueApi.php"
            UserCheck = True
        else:
            return Response({"hamkadeh : شما دستری ندارید"}, status=status.HTTP_403_FORBIDDEN)

    if company == "hamkadeh":
        if user.isAddToLineHamkadeh:
            url= "https://46.32.25.74:22428/Api/QueueApi.php"
            UserCheck = True
        else:
            return Response({"hamkadeh : شما دستری ندارید"}, status=status.HTTP_403_FORBIDDEN)


    if UserCheck:

        df = pd.read_excel(excel)

        if "code" not in df.columns:
            return Response({"فرمت اشتباه می باشد"}, status=status.HTTP_400_BAD_REQUEST)
        
        df = df[["code"]]

        ListSend =[]

        for i in range(len(df)):
            Actions ="addmember"
            Line ="80000"
            Peer = f"{df.loc[i, 'code']}"
            requestSend = requests.post(f"{url}?Action={Actions}&ExtensionNumber={Peer}&QueueNumber={Line}" , verify=False) 
            if requestSend.status_code == 200:
                ListSend.append(Peer)
        return Response({f"done : {ListSend} "}, status=status.HTTP_200_OK)













@api_view(['POST'])
def PeerToLine(request):
    
    data = request.data

    user = request.user

    Actions = data['Actions']

    Peer = data['Peer']

    Line = data['Line']

    Company = data['Company']


    if Company == 'hamkadeh':
            if user.isAddToLineHamkadeh :
                hamkadeh = requests.post(f"https://46.32.25.74:22428/Api/QueueApi.php?Action={Actions}&ExtensionNumber={Peer}&QueueNumber={Line}" , verify=False) 
                if hamkadeh.status_code == 200:
                    return Response({f"hamkadeh : {hamkadeh}"}, status=status.HTTP_200_OK)
                else:
                    return Response({"hamkadeh : error"}, status=status.HTTP_504_GATEWAY_TIMEOUT)
            else:
                return Response({"hamkadeh : شما دستری ندارید"}, status=status.HTTP_403_FORBIDDEN)

    elif Company == 'sale-hamkadeh':
        if user.isAddToLineSaleHamkadeh:
            SaleHamkadeh = requests.post(f"https://46.32.25.74:22425/Api/QueueApi.php?Action={Actions}&ExtensionNumber={Peer}&QueueNumber={Line}" , verify=False) 
            if SaleHamkadeh.status_code == 200:
                return Response({f"SaleHamkadeh : {SaleHamkadeh}"}, status=status.HTTP_200_OK)
            else:
                return Response({"SaleHamkadeh : error"}, status=status.HTTP_504_GATEWAY_TIMEOUT)

    elif Company == '5040':
        if user.isAddToLine5040 :
            F5040    = requests.post(f"https://46.32.25.74:22430/Api/QueueApi.php?Action={Actions}&ExtensionNumber={Peer}&QueueNumber={Line}" , verify=False)  
            if F5040.status_code == 200:
                return Response({f"5040 : {F5040} "}, status=status.HTTP_200_OK)
            else:
                return Response({f"5040 : error = {F5040.status_code} {F5040.text}   "}, status=status.HTTP_504_GATEWAY_TIMEOUT)
            





@api_view(['POST'])
def PeerRemoveLine(request):
    data = request.data
    user = request.user
    print(data)
    Actions = "removemember"
    Line = "80000"
    for i in data:
        hamkadeh = requests.post(f"https://46.32.25.74:22428/Api/QueueApi.php?Action={Actions}&ExtensionNumber={i}&QueueNumber={Line}" , verify=False) 
        MemberFellows.objects.filter(number = i).delete()
    
    return Response({f"hamkadeh ok"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def PeerRemoveLine5040(request):
    data = request.data
    user = request.user
    print(data)
    Actions = "removemember"
    Line = "80000"
    for i in data:
        hamkadeh = requests.post(f"https://46.32.25.74:22430/Api/QueueApi.php?Action={Actions}&ExtensionNumber={i}&QueueNumber={Line}" , verify=False) 
        Member5040.objects.filter(number = i).delete()
    return Response({f"hamkadeh ok"}, status=status.HTTP_200_OK)
                    
@api_view(['POST'])
def PeerRemoveLineSaleHamkadeh(request):
    data = request.data
    user = request.user
    print(data)
    Actions = "removemember"
    Line = "80000"
    for i in data:
        hamkadeh = requests.post(f"https://46.32.25.74:22425/Api/QueueApi.php?Action={Actions}&ExtensionNumber={i}&QueueNumber={Line}" , verify=False) 
        MemberFellows.objects.filter(number = i).delete()
    
    
    return Response({f"hamkadeh ok"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def ActiveChannelsViews(request):
    
    data = request.data
    AddItem = data['data']

    channel_layer = get_channel_layer()
 
    print(Fore.BLUE + "============ Active Channels ==============")
    
    AddItem = data['data']  

    items_to_create = []    
    exitItem = False
    for i in AddItem:
        existing_item = ActiveChannels.objects.filter(channel=i['channel'])
        if not existing_item.exists():
            exitItem = True
            print(i)
            break

    if exitItem :
        ActiveChannels.objects.all().delete()   
        print(Fore.BLUE + "deleted")


        nowTime = datetime.now()
        now = nowTime.strftime("%H:%M:%S")

        print(now)
        
        items_to_create = [ActiveChannels(channel=i['channel'] , status=i['status'] ,callerID = i["callerID"],extension =i['extension'] , duration = i['duration'] ,dateUpdate =now) for i in AddItem]
        ActiveChannels.objects.bulk_create(items_to_create)

        ActiveChannelsData = [{'channel': i['channel'] ,'extension': i['extension'] , 'status':i['status'] ,"callerID" : i["callerID"] ,'duration': i['duration'] , 'dateUpdate': now} for i in AddItem]
        async_to_sync(channel_layer.group_send)(
        "ActiveChannels_channels",
            {
                "type": "data_ActiveChannels_channels",
                "data": ActiveChannelsData,
            },
        )

    
    nowTime = datetime.now()

    now = nowTime.strftime("%Y-%m-%d %H:%M:%S")

    print(Fore.YELLOW + f"{now}")

    print(Fore.BLUE + "done")
    print(Fore.BLUE + "======= Active Channels  End =========")


    return Response('ok')



   



@api_view(['POST'])
def PeersViews(request):
    
    data = request.data
    AddItem = data['data']

    channel_layer = get_channel_layer()
 
    print(Fore.BLUE + "============ Peers ==============")
    
    AddItem = data['data']  

    items_to_create = []    
    exitItem = False
    for i in AddItem:
        existing_item = Peers.objects.filter(name=i['name'] , status =i['status'])
        if not existing_item.exists():
            exitItem = True
            print(i)
            break

    if exitItem :
        Peers.objects.all().delete()   
        print(Fore.BLUE + "deleted")


        nowTime = datetime.now()
        now = nowTime.strftime("%H:%M:%S")
        
        items_to_create = [Peers(name=i['name'] , status =i['status'] ,dateUpdate =now) for i in AddItem]
        Peers.objects.bulk_create(items_to_create)

        PeersData = [{'name': i['name'] ,'status': i['status'] , 'dateUpdate': now} for i in AddItem]
        async_to_sync(channel_layer.group_send)(
        "Peers_channels",
            {
                "type": "data_peers",
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

  
    print(Fore.BLUE + "============ Queue ==============")



    if len(CallersData) ==0 :
        caller_data = [{'name': i['code'], 'wait': i['wait'] , 'dateUpdate' : now} for i in CallersData]
        Callers.objects.all().delete()   
        async_to_sync(channel_layer.group_send)(
        "caller_channels",
            {
                "type": "data_caller_channels",
                "data": caller_data,
            },
        )
        print(Fore.YELLOW + "no caller")
        
    if len(MemberData) ==0 :
        member_data = [{'number': i['code'], 'status': i['status']} for i in MemberData]
        Member.objects.all().delete()   
        async_to_sync(channel_layer.group_send)(
        "member_channels",
            {
                "type": "data_member_channels",
                "data": member_data,
            },
        )
        print(Fore.YELLOW + "no member")

    #Member
    for m in MemberData :
        exist_member_item = Member.objects.filter(number=m['code'] , status =m['status'] )
        if not exist_member_item.exists():
            exitMemberData = True
            print(f"member  : {m}")
            break

    if  exitMemberData:
        Member.objects.all().delete()   

        print("member deleted")

        member_items_to_create = [Member(number=i['code'] , status=i['status'] ) for i in MemberData]
        Member.objects.bulk_create(member_items_to_create)
        member_data = [{'number': i['code'], 'status': i['status']} for i in MemberData]
        async_to_sync(channel_layer.group_send)(
        "member_channels",
            {
                "type": "data_member_channels",
                "data": member_data,
            },
        )
        print("member_exist_done")





    #Caller

    for c in CallersData :
        exit_Callers_item = Callers.objects.filter(name=c['code'])
        if not exit_Callers_item.exists():
            exitCallerData = True
            print(f"caller : {c}")
            break

    if exitCallerData:
        Callers.objects.all().delete()  
        
        print("caller deleted")

        Caller_items_to_create = [Callers(name=i['code'] , wait=i['wait'] , dateUpdate =now) for i in CallersData]
        Callers.objects.bulk_create(Caller_items_to_create)
        
        caller_data = [{'name': i['code'], 'wait': i['wait'] , 'dateUpdate' : now} for i in CallersData]
        async_to_sync(channel_layer.group_send)(
        "caller_channels",
            {
                "type": "data_caller_channels",
                "data": caller_data,
            },
        )
        print("caller_exist_done")
    nowTime = datetime.now()

    now = nowTime.strftime("%Y-%m-%d %H:%M:%S")

    print(Fore.YELLOW + f"{now}")

    print(Fore.BLUE + "======= End =========")

    return Response('ok')


class Index(View):
    def get(self , request):
        context ={
            'test' : 'Hello word'
        }
        return render(request , 'test.html')



class Test(CreateAPIView):
    queryset =ActiveChannels.objects.all() 
    serializer_class =ActiveChannelsSerializer
    # def dispatch(self, request, *args, **kwargs):
    #     response = super().dispatch(request, *args, **kwargs)
    #     response['Access-Control-Allow-Origin'] = '*'
    #     return response





















    
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
















