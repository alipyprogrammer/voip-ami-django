from django.db import models

class QueueLog(models.Model):
    id       = models.BigAutoField(primary_key=True)
    idd       = models.CharField(max_length=50 , default="")
    time      = models.DateTimeField()
    callid    = models.CharField(max_length=40, default='')
    queuename = models.CharField(max_length=20, null=True , blank=True)
    serverid  = models.CharField(max_length=20, null=True , blank=True)
    agent     = models.CharField(max_length=40, null=True , blank=True)
    event     = models.CharField(max_length=20, null=True , blank=True)
    data1     = models.CharField(max_length=40,null=True , blank=True)
    data2     = models.CharField(max_length=40,null=True , blank=True)
    data3     = models.CharField(max_length=40,null=True , blank=True)
    data4     = models.CharField(max_length=40,null=True , blank=True)
    data5     = models.CharField(max_length=40,null=True , blank=True)


class QueueLoghamkadeh(models.Model):
    id       = models.BigAutoField(primary_key=True)
    idd       = models.CharField(max_length=50 , default="")
    time      = models.DateTimeField()
    callid    = models.CharField(max_length=40, default='')
    queuename = models.CharField(max_length=20, null=True , blank=True)
    serverid  = models.CharField(max_length=20, null=True , blank=True)
    agent     = models.CharField(max_length=40, null=True , blank=True)
    event     = models.CharField(max_length=20, null=True , blank=True)
    data1     = models.CharField(max_length=40,null=True , blank=True)
    data2     = models.CharField(max_length=40,null=True , blank=True)
    data3     = models.CharField(max_length=40,null=True , blank=True)
    data4     = models.CharField(max_length=40,null=True , blank=True)
    data5     = models.CharField(max_length=40,null=True , blank=True)

    