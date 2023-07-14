from django.db import models
from django.utils import timezone

# Create your models here.
class Request(models.Model):
      request_id = models.CharField(max_length=14, unique=True)
      requester = models.CharField(max_length=255)
      system = models.ManyToManyField(Invensys)
      date = models.DateTimeField(defaut=timezone.now)
      remakrs=models.TextField(default='', blank=True)


      def __str__(self):
            return(self.request_id)