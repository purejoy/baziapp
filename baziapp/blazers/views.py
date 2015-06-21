# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from bazi import Bazi
from bazi import ast
from bazi.baziforms.forms import BaziForm
from wx import wx
import datetime 
#import random
#import string
#import hashlib
#import os
#import urllib2
#from django.core.cache import cache


def contact(request):
    return render_to_response('contact.html')

def about(request):
    return render_to_response('about.html')


def post(request):
    
    url = request.build_absolute_uri()
    sign = wx.getSign(url)
    signature = sign['signature']
    noncestr = sign['nonceStr']
    timestamp = sign['timestamp']

    if request.method == 'GET':
        form = BaziForm()
    else:
        form = BaziForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            entries = []
            gender = cd['gender']
            date = cd['date']
            time = cd['time']
            ztytoggle = 0
            pqtoggle = 0
            xltoggle = 0
            lifaindx = 0
            L = 120
            bd = datetime.datetime(date.year,date.month,date.day,time.hour,time.minute)
            if 'xltoggle' in request.POST:
                xltoggle = 1
                onehour = datetime.timedelta(hours=1)
                bd -= onehour
            #e8dt = ztydt
            dtstr = date.isoformat().split("T")[0]
            filename = "%s_%s" %(dtstr, time.strftime("%H:%M"))
            qrargs = "qrargs=%s_%s" %(gender, filename)
            

            if 'ztytoggle' in request.POST:
                ztytoggle = 1
                L = eval(request.POST.get('lonlat',''))
                qrargs += "_%s" %(L)
            else:
                qrargs += "_L"
                
            if 'pqtoggle' in request.POST:
                pqtoggle = 1
                lifaindx = eval(request.POST.get('lifa','')) + 1
                qrargs += "_%s" %(lifaindx-1)
            else:
                qrargs += "_P"

            if xltoggle == 1:
                qrargs += "_1"
            else:
                qrargs += "_X"
            
            baziinst = Bazi.bazi(bd,eval(gender),ztytoggle,L,lifaindx)
            baziinst.Paipan()
            #bazidesc = baziinst.Get8zi()
            #dtstr = date.isoformat().split("T")[0]
            #queryargs = u"gender=%s&date=%s&time=%s" %(gender,dtstr,time.strftime("%H:%M"))
            #qrargs = "qrargs=%s.%s.%s" %(gender, dtstr, time.strftime("%H:%M"))
            return render(request,"getbazi.html",
                          { 'baziinst':baziinst,'timestamp':timestamp,'noncestr':noncestr,'signature':signature,'filename':filename,
                            'ztytoggle':ztytoggle,'xltoggle':xltoggle,'pqtoggle':pqtoggle,'qrargs':qrargs },
                          context_instance=RequestContext(request))


    return render(request,"bazi.html",locals(),context_instance=RequestContext(request))


def query(request):  
    url = request.build_absolute_uri()
    sign = wx.getSign(url)
    signature = sign['signature']
    noncestr = sign['nonceStr']
    timestamp = sign['timestamp']

    if 'gender' in request.GET or 'date' in request.GET or 'time' in request.GET:
        form = BaziForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            gender = cd['gender']
            date = cd['date']
            time = cd['time']
            ztytoggle = 0
            pqtoggle = 0
            xltoggle = 0
            lifaindx = 0
            L = 120
            bd = datetime.datetime(date.year,date.month,date.day,time.hour,time.minute)
            if 'xltoggle' in request.GET:
                xltoggle = 1
                onehour = datetime.timedelta(hours=1)
                bd -= onehour
                
            dtstr = date.isoformat().split("T")[0]
            filename = "%s_%s" %(dtstr, time.strftime("%H:%M"))
            qrargs = "qrargs=%s_%s" %(gender, filename)
            #qrargs = "qrargs=%s_%s_%s" %(gender, dtstr, time.strftime("%H:%M"))

            if 'ztytoggle' in request.GET:
                ztytoggle = 1
                L = eval(request.GET.get('lonlat',''))
                qrargs += "_%s" %(L)
                #return HttpResponse("经度=%s" %(L))
                #return HttpResponse(zty.calc_zty(e8dt,L))
            else:
                qrargs += "_L"
                
            if 'pqtoggle' in request.GET:
                pqtoggle = 1
                lifaindx = eval(request.GET.get('lifa','')) + 1
                qrargs += "_%s" %(lifaindx-1)
            else:
                qrargs += "_P"

            if xltoggle == 1:
                qrargs += "_1"
            else:
                qrargs += "_X"
            
            baziinst = Bazi.bazi(bd,eval(gender),ztytoggle,L,lifaindx)
            baziinst.Paipan()
            #bazidesc = baziinst.Get8zi()
            #dtstr = date.isoformat().split("T")[0]
            #queryargs = u"gender=%s&date=%s&time=%s" %(gender,dtstr,time.strftime("%H:%M"))
            #qrargs = "qrargs=%s.%s.%s" %(gender, dtstr, time.strftime("%H:%M"))
            #return HttpResponse(qrargs)
            return render(request,"getbazi.html",
                          { 'baziinst':baziinst,'timestamp':timestamp,'noncestr':noncestr,'signature':signature,'filename':filename,
                            'ztytoggle':ztytoggle,'xltoggle':xltoggle,'pqtoggle':pqtoggle,'qrargs':qrargs},
                          context_instance=RequestContext(request))
        else:
            return render(request,"query.html",locals(),context_instance=RequestContext(request))
       
    form = BaziForm()
    return render(request,"query.html",locals(),context_instance=RequestContext(request))


def qrquery(request):
    url = request.build_absolute_uri()
    sign = wx.getSign(url)
    signature = sign['signature']
    noncestr = sign['nonceStr']
    timestamp = sign['timestamp']
    if 'qrargs' in request.GET and request.GET['qrargs']:
        arglist = str(request.GET['qrargs']).split('_')
        if len(arglist) == 6 and arglist[0] == '0' or arglist[0] == '1':
            arglist[1] += " " + arglist[2]
            try:
                bd = datetime.datetime.strptime(arglist[1],"%Y-%m-%d %H:%M")
            except ValueError:
                form = BaziForm()
                return render(request,"query.html",locals(),context_instance=RequestContext(request))

            else:
                filename = arglist[1]
                gender = eval(arglist[0])
                if arglist[5] == "X":
                    xltoggle = 0
                else:
                    xltoggle = 1
                    onhour = datetime.timedelta(hours=1)
                    bd -= onhour

                if arglist[3] == "L":
                    ztytoggle = 0
                    L = 120
                else:
                    ztytoggle = 1
                    L = eval(arglist[3])
   
                if arglist[4] == "P":
                    pqtoggle = 0
                    lifa = 0
                else:
                    pqtoggle = 1
                    lifa = eval(arglist[4])+1

  
                baziinst = Bazi.bazi(bd,eval(gender),ztytoggle,L,lifaindx)
                baziinst.Paipan()
                qrargs = "qrargs=%s" %(str(request.GET['qrargs']))
            	return render(request,"getbazi.html",
                              {'baziinst':baziinst,'timestamp':timestamp,'noncestr':noncestr,'signature':signature,'filename':filename,
                               'ztytoggle':ztytoggle,'xltoggle':xltoggle,'pqtoggle':pqtoggle,'qrargs':qrargs},
                              context_instance=RequestContext(request))

    form = BaziForm()
    return render(request,"query.html",locals(),context_instance=RequestContext(request))





    

    
