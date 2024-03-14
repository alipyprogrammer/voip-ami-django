from pyexpat import model
from statistics import mode
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import os


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext
# ==============================================


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.name}{ext}"
    return f"user/{final_name}"


def upload_User_image_path_hamkadeh(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.idd}-{ext}"
    return f"hamkadeh/{final_name}"


def upload_User_image_path_5040(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.idd}-{ext}"
    return f"5040/{final_name}"



class Age(models.Model):
    Age = models.CharField(max_length=50 , verbose_name='سن')





class User(AbstractUser):
 
    name                    = models.CharField(max_length=40 ,null=True , blank=True)
    phoneNumber             = models.CharField(max_length=11 ,null=True , blank=True,verbose_name='شماره تلفن')
    Image                   = models.ImageField(upload_to =upload_image_path ,null=True , blank=True )
    Address                 = models.TextField(max_length=200, verbose_name='آدرس' ,null=True , blank=True)
    sex                     = models.CharField(max_length=10, null=True , blank =True)
    City                    = models.CharField(max_length=6 , null=True , blank=True) 
    birthday                = models.CharField(max_length=100,null=True , blank=True) 
    ActiveUser              = models.CharField(max_length=150 , null=True , blank=True, verbose_name='فعال بودن کاربر ')  
    job                     = models.CharField(max_length=100,null=True , blank=True) 

    internal                = models.CharField(max_length=10 , null=True , blank=True)
    Manager                 = models.BooleanField(default=False)
    isForward               = models.BooleanField(default=False) 

    #Hamkadeh
    isForwardHamkadeh        = models.BooleanField(default=False) 
    isMonitoringHamkadeh     = models.BooleanField(default=False)
    isAddToLineHamkadeh      = models.BooleanField(default=False)
    isListeningHamkadeh      = models.BooleanField(default=False)
    robotHamkadeh            = models.BooleanField(default=False)
    statusConsultantHamkadeh = models.BooleanField(default=False)
    robotVoip                = models.BooleanField(default=False)

    #SaleHamkadeh
    isForwardSaleHamkadeh       = models.BooleanField(default=False) 
    isMonitoringSaleHamkadeh    = models.BooleanField(default=False)
    isAddToLineSaleHamkadeh     = models.BooleanField(default=False)
    isListeningSaleHamkadeh     = models.BooleanField(default=False)
    statusSupportHamkadeh       = models.BooleanField(default=False)
    #5040
    isForward5040           = models.BooleanField(default=False) 
    isMonitoring5040        = models.BooleanField(default=False)
    isAddToLine5040         = models.BooleanField(default=False)
    isListening5040         = models.BooleanField(default=False)
    robot5040               = models.BooleanField(default=False)
    statusUser5040          = models.BooleanField(default=False)





class Users5040(models.Model):
    consultant_idd      = models.CharField(max_length = 85 , null=True , blank=True )
    support_idd         = models.CharField(max_length = 85 , null=True , blank=True )
    operator_number     = models.CharField(max_length = 11  , null=True , blank=True)
    name                = models.CharField(max_length = 85 )
    profile             = models.CharField(max_length=250  ,null=True , blank=True )
    status              = models.IntegerField(default=0)
class UsersHamkadeh(models.Model):
    consultant_idd      = models.CharField(max_length = 85 , null=True , blank=True )
    support_idd         = models.CharField(max_length = 85 , null=True , blank=True )
    operator_number            = models.CharField(max_length = 11  , null=True , blank=True)
    name                = models.CharField(max_length = 85 )
    profile             = models.CharField(max_length=250  ,null=True , blank=True )
    status              = models.IntegerField(default=0)

    def __str__(self):
        if self.consultant_idd is not None:
            return self.consultant_idd
        else:
            return self.support_idd

    # class Meta:    
        # database = 'hamkadeh'



  
