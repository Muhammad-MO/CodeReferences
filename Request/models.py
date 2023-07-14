from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

STATUS_CHOICES = (
   ('Pending', 'pending'),
   ('Approve', 'Approve'),
   ('In-Progress', 'In-progress'),

)

def validate_OverallRequest_status(value):
    if value not in dict(STATUS_CHOICES):
        raise ValidationError(('%(value) is incorrect status.'), params={'value':value},)
    
class Request(models.Model):
    request_id = models.Charfield(max_langth=14, unique=True)
    requester = models.Chafield(max_langth=255)
    fqdn = models.Charfield(max_length=255)
    appcode = models.Charfield(max_langth=255)
    zone = models.Charfield(max_length=255)
    lob = models.Charfield(max_length=255)
    system = models.ManyToManyField(Invensys)
    environment = models.Charfield(max_length=200)
    requested_date = models.Charfield(max_length=255)
    approved_date = models.DateTimeField(blank=True, null=True)
    completed_date = models.DateTimeField(blank=True, null=True)
    approver = models.CharField(max_length=200 blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES,default='Pending')
    remarks = models.TextField(default='', blank=True)

    def __str__(self):
        return(self.request_id)
