from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect,HttpResponse, HttpResponsePermanentRedirect,rever, get_list_or_404, 
from django.conf import settings
from.models import Request
from .import utils
from django.contrib import messages
from API import email
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from app.models import *
from app.utils import *
from app.views import saveAppcodeData


@login_required
def createrequest(request):
    if request.method == "POST":
        output = handlePOST(request)
        return output
    
    data = {}
    data['appcode'] = list(Application.objects.all().values_list('appcode', flat=True))
    data['environment'] = list(Subnet.objects.all().values_list('environment', flat=True).distinct()) #use distinct to filter only unique values when fetching data
    data['zone'] = list(Subnet.objects.all().values_list('zone', flat=True).distinct())  
    data['base_path'] = '/' + str(settings.BASE_PATH)       
    return render(request, "request_ip_form.html",data)                 