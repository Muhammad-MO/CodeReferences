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
import logging
from app.views import saveAppcodeData
from rest_framework import APIviews

logger = logging.getLogger('system')
class F5error(Exception):


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

def handlePOST(request):
    try:

        data_output={}
        data_output['fqdn'] = request.POST.get('fqdn')
        data_output['appcode'] = request.POST.get('appcode')
        data_output['environment'] = request.POST.get('environment')
        data_output['zone'] = request.POST.get('zone')
        data_output['Invensys'] = request.POST.getlist('multiselect1_to')
        data_output['lob'] = request.POST.getlist('lob')
        fqdn = data_output['fqdn']
        appcode = data_output['appcode']
        lob = data_output['lob']
        environment = data_output['environment']
        zone = data_output['zone']
        server = data_output['Invensys']
        requster = request.user.full_name
        domainlist = list(ApprovedDomain.objects.values_list('name', flat=True))
        domain_found = False
        for eachdomain in domainlist:
            if eachdomain in fqdn:
                domain_found = True
                break
        if not domain_found:
            raise F5error("FQDN not part of approved domain")
        if not Application.objects.filter(appcode=appcode).exists():
             raise F5error("appcode does not exist")
        
        if not LOB.objects.filter(name=lob).exists():
             raise F5error("LOB does not exist")
        
        if not Subnet.objects.filter(environment=environment).exists():
             raise F5error("environment does not exist")
        
        if not Subnet.objects.filter(zone=zone).exists():
             raise F5error("zone does not exist")
        for eachservers in server:
            if not Invensys.objects.filter(hostname=eachservers).exist():
                raise F5error('Wrong list of servers')
        output = utils.createrequest(data=data_output, requester=request.user.full_name)
        email.send_request_email(fqdn=fqdn, appcode=appcode,zone=zone, lob=lob,environment=environment,user=request.user)
        return render(request, "request_ip_form.html")
        
    except Exception as e:
        print("error encountered")
        print(str(e))
        logger.exception(str(e))
        return JsonResponse({"message":str(e)})
    
@login_required
def viewrequests(request):

    data_output={}
    all_request = Request.objects.all()
    all_request_list = []
    for request_info in all_request:
        data_output = {}
        data_output['fqdn'] = request_info.fqdn
        data_output['appcode'] = request_info.appcode
        data_output['lob'] = request_info.lob
        data_output['environment'] = request_info.environment
        data_output['zone'] = request_info.zone
        data_output['request_id'] = request_info.request_id
        data_output['requester'] = request_info.requester
        invensys_data = request_info.system.values()
        invensys_info = []
        for data in invensys_data:
             invensys_info.append(data['hostname'])
             data_output['system'] = invensys_info
             all_request_list.append(data_output)
             print(all_request_list)
             return render(request, "viewrequest.html",{"viewrequest":all_request_list})
        
class Invensysdata(APIView):
    http_method_names = ['get', 'options']
    def get(self, request, **kwargs):
     try:
         
    appcode = request.GET.get('appcode','')
    environment = request.GET.get('environment', '')
    zone = request.GET.get('zone', '')
    serverlist=Serverdata(environment,zone,appcode)
    return Response(serverlist, status=http_status.HTTP_200_OK)

    except Exception as e:

    logger.exception(str(e)):
    return Response('An error occured: {0}'.format(str(e)), status=http_status.HTTP_500_INTERNAL_SEVER_ERROR)


class Appcodelob(APIView)

      http_method_names = ['get', 'options']
      def get(self, request, **kwargs):
        try:
            
            appcode = request.GET.get('appcode', '')
            appcode_lob_list = Application.objects.filter(appcode=appcode)
            appcode1 = appcode_lob_list[0]
            lobdata = {'lob':appcode1.lob.name}
            return Reponse(lobdata, status=http_status.HTTP_200_OK)
        except Exception as e:
            logger.exception(str(e))
            return Response("An error occured:{0}").format(str(e),status=http_status.HTTP_500_INTERNAL_SEVER_ERROR)

def Serverdata(environment, zone, appcode):
    serverinfo_list = Invensys.objects.filter(appcode_appcode=appcode, environment=environment,zone=zone)
    serverlist=[]
    for servers in serverinfo_list:
        serverlist.append(server.hostname)
    print(serverlist)
    return serverlist

class Requestdetails(APIView):
    http_method_names = ['get', 'kwargs']
    def get(self, request, **kwargs):
        try:
            requestid = request.GET.get("request_id", '')
            requestdetail = Request.objects.get(request_id=requestid)
            eachrequest = {

                    'Appcode':requestdetail.appcode,
                    'FQDN':requestdetail.fqdn,
                    'Environment':requestdetail.environment,
                    'Zone':requestdetail.zone,
                    'Lob':requestdetail.lob,
                    'Requestid':requestdetail.request_id,
                    'Requester':requestdetail.requester,
                    'Requested Data':requestdetail.requested_data,

            }

            return Response(eachrequest, status=http_status.HTTP_200_OK)
        except Exception as e:
            logger.exception(str(e))
        return Response("An error occured:{0}").format(str(e),status=http_status.HTTP_500_INTERNAL_SEVER_ERROR)

    


        
        




         
        





