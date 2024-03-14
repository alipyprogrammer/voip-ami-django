from django.db import models

from asgiref.sync import async_to_sync
# Create your models here.
from channels.layers import get_channel_layer













class Forward(models.Model):
    extension      = models.CharField(max_length=10 , null=True ,blank=True)
    actions        = models.CharField(max_length=5 ,null=True , blank=True)
    mobileForward  = models.CharField(max_length=25 , null=True , blank=True)
    flag           = models.CharField(max_length=5 , null=True , blank=True )
    date           = models.DateTimeField(auto_now=True)
    company        = models.CharField(max_length=30 , null=True , blank=True)
    actions        = models.CharField(max_length=10 , null=True , blank=True)
    idInternal     = models.CharField(max_length=7 , null=True , blank=True)
    def __str__(self):
        return self.extension












# hamkadeh ==========================

class ActiveChannels(models.Model):
    channel    =  models.CharField(max_length=200 , null=True , blank=True)
    dateUpdate =  models.CharField(max_length=50 , default='' , null=True , blank=True)
    extension =  models.CharField(max_length=50 , default='' , null=True , blank=True)
    duration =  models.CharField(max_length=50 , default='' , null=True , blank=True)
    callerID =  models.CharField(max_length=50 , default='' , null=True , blank=True)
    status   = models.CharField(max_length =50 ,default='' ,null=True , blank=True)

    def __str__(self):
        return self.number
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_data_update()

    def delete(self, *args, **kwargs):
        self.send_data_update()
        super().delete(*args, **kwargs)

    def send_data_update(self):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        ActiveChannels_data = [{"channel": Active.channel  , "status" : Active.status, "callerID" : Active.callerID ,"dateUpdate" :Active.dateUpdate,"extension" :Active.extension,"duration" :Active.duration,
        } for Active in ActiveChannels.objects.all()]
        async_to_sync(channel_layer.group_send)(
            "ActiveChannels_channels",
            {
                "type": "data_ActiveChannels_channels",
                "data": ActiveChannels_data,
            },
        )
    


    def __str__(self):
        return self.channel







class Peers(models.Model):
    name   = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    dateUpdate = models.CharField(max_length=50 , default='' , null=True , blank=True)
    
    def __str__(self):
        return self.name


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_data_update()

    def delete(self, *args, **kwargs):
        self.send_data_update()
        super().delete(*args, **kwargs)

    def send_data_update(self):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        Peers_Channels = [{"name": peers.name ,  "status" : peers.status}  for peers in Peers.objects.all()]
        async_to_sync(channel_layer.group_send)(
            "Peers_channels",
            {
                "type": "data_peers",
                "data": Peers_Channels,
            },
        )




class Member(models.Model):
    number  = models.CharField(max_length=60)
    Time    = models.CharField(max_length=150 , default='')
    status  = models.CharField(max_length=25)
    def __str__(self):
        return self.number
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_data_update()

    def delete(self, *args, **kwargs):
        self.send_data_update()
        super().delete(*args, **kwargs)

    def send_data_update(self):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        Member_data = [{"number": member.number, "status": member.status} for member in Member.objects.all()]
        async_to_sync(channel_layer.group_send)(
            "member_channels",
            {
                "type": "data_member_channels",
                "data": Member_data,
            },
        )
    

class Callers(models.Model):
    name = models.CharField(max_length=150)
    wait = models.CharField(max_length=10)
    dateUpdate = models.CharField(max_length=150 , default='')
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_data_update()

    def delete(self, *args, **kwargs):
        self.send_data_update()
        super().delete(*args, **kwargs)

    def send_data_update(self):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        callers_data = [{"name": caller.name, "wait": caller.wait , "dateUpdate" : caller.dateUpdate} for caller in Callers.objects.all()]
        async_to_sync(channel_layer.group_send)(
            "caller_channels",
            {
                "type": "data_caller_channels",
                "data": callers_data,
            },
        )










########5040#####

class Peers5040(models.Model):
    name   = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    dateUpdate = models.CharField(max_length=50 , default='' , null=True , blank=True)
    
    def __str__(self):
        return self.name


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_data_update()

    def delete(self, *args, **kwargs):
        self.send_data_update()
        super().delete(*args, **kwargs)

    def send_data_update(self):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        Peers_Channels = [{"name": peers.name ,  "status" : peers.status}  for peers in Peers.objects.all()]
        async_to_sync(channel_layer.group_send)(
            "Peers_channels_5040",
            {
                "type": "data_peers_5040",
                "data": Peers_Channels,
            },
        )



class Member5040(models.Model):
    number  = models.CharField(max_length=60)
    Time    = models.CharField(max_length=150 , default='')
    status  = models.CharField(max_length=25)
    def __str__(self):
        return self.number
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_data_update()

    def delete(self, *args, **kwargs):
        self.send_data_update()
        super().delete(*args, **kwargs)

    def send_data_update(self):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        Member_data = [{"number": member.number, "status": member.status} for member in Member.objects.all()]
        async_to_sync(channel_layer.group_send)(
            "member_channels_5040",
            {
                "type": "data_member_channels_5040",
                "data": Member_data,
            },
        )
    

class Callers5040(models.Model):
    name = models.CharField(max_length=150)
    wait = models.CharField(max_length=10)
    dateUpdate = models.CharField(max_length=150 , default='')
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_data_update()

    def delete(self, *args, **kwargs):
        self.send_data_update()
        super().delete(*args, **kwargs)

    def send_data_update(self):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        callers_data = [{"name": caller.name, "wait": caller.wait , "dateUpdate" : caller.dateUpdate} for caller in Callers.objects.all()]
        async_to_sync(channel_layer.group_send)(
            "caller_channels_5040",
            {
                "type": "data_caller_channels_5040",
                "data": callers_data,
            },
        )








class ActiveChannels5040(models.Model):
    channel    =  models.CharField(max_length=200 , null=True , blank=True)
    dateUpdate =  models.CharField(max_length=50 , default='' , null=True , blank=True)
    extension =  models.CharField(max_length=50 , default='' , null=True , blank=True)
    duration =  models.CharField(max_length=50 , default='' , null=True , blank=True)
    callerID =  models.CharField(max_length=50 , default='' , null=True , blank=True)
    status   = models.CharField(max_length =50 ,default='' ,null=True , blank=True)

    def __str__(self):
        return self.number
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_data_update()

    def delete(self, *args, **kwargs):
        self.send_data_update()
        super().delete(*args, **kwargs)

    def send_data_update(self):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        ActiveChannels5040_data = [{"channel": Active.channel ,"status" :Active.status ,"callerID" : Active.callerID ,"dateUpdate" :Active.dateUpdate,"extension" :Active.extension,"duration" :Active.duration,
        } for Active in ActiveChannels5040.objects.all()]
        async_to_sync(channel_layer.group_send)(
            "ActiveChannels5040_channels",
            {
                "type": "data_ActiveChannels5040_channels",
                "data": ActiveChannels5040_data,
            },
        )
    


    def __str__(self):
        return self.channel





########Fellows hamkadeh#############



class PeersFellows(models.Model):
    name   = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    dateUpdate = models.CharField(max_length=50 , default='' , null=True , blank=True)
    
    def __str__(self):
        return self.name


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_data_update()

    def delete(self, *args, **kwargs):
        self.send_data_update()
        super().delete(*args, **kwargs)

    def send_data_update(self):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        Peers_Channels = [{"name": peers.name ,  "status" : peers.status}  for peers in Peers.objects.all()]
        async_to_sync(channel_layer.group_send)(
            "Peers_channels_Fellows",
            {
                "type": "data_peers_Fellows",
                "data": Peers_Channels,
            },
        )


class MemberFellows(models.Model):
    number  = models.CharField(max_length=60)
    Time    = models.CharField(max_length=150 , default='')
    status  = models.CharField(max_length=25)
    def __str__(self):
        return self.number
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_data_update()

    def delete(self, *args, **kwargs):
        self.send_data_update()
        super().delete(*args, **kwargs)

    def send_data_update(self):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        Member_data = [{"number": member.number, "status": member.status} for member in Member.objects.all()]
        async_to_sync(channel_layer.group_send)(
            "member_channels_Fellows",
            {
                "type": "data_member_channels_Fellows",
                "data": Member_data,
            },
        )
    

class CallersFellows(models.Model):
    name = models.CharField(max_length=150)
    wait = models.CharField(max_length=10)
    dateUpdate = models.CharField(max_length=150 , default='')
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_data_update()

    def delete(self, *args, **kwargs):
        self.send_data_update()
        super().delete(*args, **kwargs)

    def send_data_update(self):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        callers_data = [{"name": caller.name, "wait": caller.wait , "dateUpdate" : caller.dateUpdate} for caller in Callers.objects.all()]
        async_to_sync(channel_layer.group_send)(
            "caller_channels_Fellows",
            {
                "type": "data_caller_channels_Fellows",
                "data": callers_data,
            },
        )


class ActiveChannelsFellows(models.Model):
    channel    =  models.CharField(max_length=200 , null=True , blank=True)
    dateUpdate =  models.CharField(max_length=50 , default='' , null=True , blank=True)
    extension =  models.CharField(max_length=50 , default='' , null=True , blank=True)
    duration =  models.CharField(max_length=50 , default='' , null=True , blank=True)
    callerID =  models.CharField(max_length=50 , default='' , null=True , blank=True)
    status   = models.CharField(max_length =50 ,default='' ,null=True , blank=True)
    

    def __str__(self):
        return self.number
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_data_update()

    def delete(self, *args, **kwargs):
        self.send_data_update()
        super().delete(*args, **kwargs)

    def send_data_update(self):
        from channels.layers import get_channel_layer
        from asgiref.sync import async_to_sync
        
        channel_layer = get_channel_layer()
        ActiveChannelsFellows_data = [{"channel": Active.channel , "status":Active.status, "callerID" : Active.callerID ,"dateUpdate" :Active.dateUpdate,"extension" :Active.extension,"duration" :Active.duration,
        } for Active in ActiveChannelsFellows.objects.all()]
        async_to_sync(channel_layer.group_send)(
            "ActiveChannelsFellows_channels",
            {
                "type": "data_ActiveChannelsFellows_channels",
                "data": ActiveChannelsFellows_data,
            },
        )
    


    def __str__(self):
        return self.channel


