import json
from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
from time import sleep
from .models import *
# from .models import Room, Message
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async




class SocketConsumer(AsyncWebsocketConsumer):



    @sync_to_async
    def get_peers_data(self):
        return list(Peers.objects.all().values('name', 'status', 'dateUpdate'))

    @sync_to_async
    def get_data_member_channels(self):
        return list(Member.objects.all().values('number', 'status'))
    
    @sync_to_async
    def get_data_caller_channels(self):
        return list(Callers.objects.all().values('name', 'wait' , 'dateUpdate'))

    @sync_to_async
    def get_data_ActiveChannels_channels(self):
        return list(ActiveChannels.objects.all().values('channel' ,'status','callerID','dateUpdate','extension','duration'))



    async def connect(self):
        await self.accept()
        

        channel_layer = get_channel_layer()
    
        await self.channel_layer.group_add("caller_channels", self.channel_name)
        await self.channel_layer.group_add("member_channels", self.channel_name)
        await self.channel_layer.group_add("ActiveChannels_channels", self.channel_name)
        await self.channel_layer.group_add("Peers_channels", self.channel_name)



        PeersData = await self.get_peers_data()
        MemberData = await self.get_data_member_channels()
        CallersData = await self.get_data_caller_channels()
        ActiveChannelsData = await self.get_data_ActiveChannels_channels()

        await channel_layer.group_send(
            "Peers_channels",
            {
                "type": "data_peers",
                "data": PeersData,
            },
        )

        await channel_layer.group_send(
        "caller_channels",
            {
                "type": "data_caller_channels",
                "data": CallersData,
            },
        )

        await channel_layer.group_send(
        "ActiveChannels_channels",
            {
                "type": "data_ActiveChannels_channels",
                "data": ActiveChannelsData,
            },
        )

        await channel_layer.group_send(
            "member_channels",
                {
                    "type": "data_member_channels",
                    "data": MemberData,
                },
        )
    

    async def data_caller_channels(self, event):
        data = event['data']
        await self.send(json.dumps({'callers': data}))

    async def data_member_channels(self, event):
        data = event['data']
        await self.send(json.dumps({'member': data}))
    
    async def data_ActiveChannels_channels(self, event):
        data = event['data']
        await self.send(json.dumps({'active_channels': data}))
    
    async def data_peers(self, event):
        data = event['data']
        await self.send(json.dumps({'peers': data}))
        

    async def websocket_receive(self, event):
        pass

