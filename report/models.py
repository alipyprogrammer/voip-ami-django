from django.db import models
from User.models import *






class Report(models.Model):
    # person
    #################################
    Type_CHOICES = (
    ("call", "call"),
    ("agent", "agent"),
    )
    name                    = models.CharField(max_length=150 , null=True , blank=True)
    type                    = models.CharField(max_length=10,choices=Type_CHOICES,default="call")
    agent                   = models.TextField()
    queue_log               = models.TextField()
    author                  = models.ForeignKey(User,on_delete=models.CASCADE, null=True , blank=True)
    
    
    def __str__(self):
        return  self.name
    