import json
from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
from time import sleep
from voip.models import *
# from .models import Room, Message
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from User.permissions import IsManager
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from User.models import User






class SocketConsumer(AsyncWebsocketConsumer):



    @sync_to_async
    def get_peers_data(self):
        return list(Peers5040.objects.all().values('name', 'status', 'dateUpdate'))

    @sync_to_async
    def get_data_member_channels(self):
        return list(Member5040.objects.all().values('number', 'status'))
    
    @sync_to_async
    def get_data_caller_channels(self):
        return list(Callers5040.objects.all().values('name', 'wait' , 'dateUpdate'))

    @sync_to_async
    def get_data_ActiveChannels5040_channels(self):
        return list(ActiveChannels5040.objects.all().values('channel','callerID','dateUpdate','extension','duration'))



    async def connect(self):
        await self.accept()
        

        channel_layer = get_channel_layer()
    
        await self.channel_layer.group_add("caller_channels_5040", self.channel_name)
        await self.channel_layer.group_add("member_channels_5040", self.channel_name)
        await self.channel_layer.group_add("ActiveChannels5040_channels", self.channel_name)
        await self.channel_layer.group_add("Peers_channels_5040", self.channel_name)



        PeersData = await self.get_peers_data()
        MemberData = await self.get_data_member_channels()
        ActiveChannels5040Data = await self.get_data_ActiveChannels5040_channels()
        CallersData = await self.get_data_caller_channels()

        await channel_layer.group_send(
            "Peers_channels_5040",
            {
                "type": "data_peers_5040",
                "data": PeersData,
            },
        )

        await channel_layer.group_send(
        "caller_channels_5040",
            {
                "type": "data_caller_channels_5040",
                "data": CallersData,
            },
        )


        await channel_layer.group_send(
        "ActiveChannels5040_channels",
            {
                "type": "data_ActiveChannels5040_channels",
                "data": ActiveChannels5040Data,
            },
        )


        await channel_layer.group_send(
            "member_channels_5040",
                {
                    "type": "data_member_channels_5040",
                    "data": MemberData,
                },
        )
    

    async def data_caller_channels_5040(self, event):
        data = event['data']
        await self.send(json.dumps({'callers': data}))

    async def data_member_channels_5040(self, event):
        data = event['data']
        await self.send(json.dumps({'member': data}))
    
    async def data_ActiveChannels5040_channels(self, event):
        data = event['data']
        await self.send(json.dumps({'active_channels': data}))
    
    async def data_peers_5040(self, event):
        data = event['data']
        await self.send(json.dumps({'peers': data}))
        

    async def websocket_receive(self, event):
        pass

