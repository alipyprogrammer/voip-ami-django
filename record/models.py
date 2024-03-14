from django.db import models
from User.models import *
# Create your models here.
from User.models import *


class LogOnlineHamkadeh(models.Model):
    idd            = models.CharField(max_length=43 , default="")
    consultant_idd  = models.ForeignKey(UsersHamkadeh, related_name ="consultant_id", on_delete=models.CASCADE , null=True , blank=True )
    support_idd     = models.ForeignKey(UsersHamkadeh, related_name ="support_id", on_delete=models.CASCADE , null=True , blank=True ) 
    status = models.CharField(max_length=85)
    date   = models.DateTimeField()

class VoipLogOnlineHamkadeh(models.Model):
    user   = models.ForeignKey(UsersHamkadeh , on_delete=models.CASCADE , null=True , blank=True )
    status = models.CharField(max_length=45)
    date   = models.DateTimeField(auto_now_add=True) 



class ReservationsHamkadeh(models.Model):
    idd            = models.CharField(max_length = 50)
    consultant_id  = models.ForeignKey(UsersHamkadeh, on_delete=models.CASCADE , null=True , blank=True )
    client_id      = models.CharField(max_length=50)
    start_date     = models.DateTimeField()
    end_date       = models.DateTimeField()
    status         = models.CharField(max_length=50)
    created_at     = models.DateTimeField()
    updated_at     = models.DateTimeField()