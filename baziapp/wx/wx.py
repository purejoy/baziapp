# -*- coding:utf-8 -*-
import time
import random
import string
import hashlib
import os
import urllib2,json
from django.core.cache import cache



def getAccesstoken():
    access_token = cache.get('access_token')
    if access_token:
        return access_token
    res = urllib2.urlopen("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=填写自己的appid&secret=填写自己的密钥")
    accesstokenDict = json.loads(res.read())
    access_token = accesstokenDict['access_token']
    expire_time = accesstokenDict['expires_in']
    cache.set('access_token',access_token,timeout = expire_time)
    return access_token

def getJsApiTicket(accesstoken):
    ticket = cache.get('jsapi_ticket')
    if ticket:
        return ticket
    res = urllib2.urlopen("https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi" %(accesstoken))
    response = res.read()
    ticketDict = json.loads(response)
    if ticketDict['errcode'] != 0:
        raise Exception
    ticket = ticketDict['ticket']
    expires_in = ticketDict['expires_in']
    cache.set('jsapi_ticket',ticket,timeout = expires_in)
    return ticket

def getSign(url):
    timestamp = int(1000 * time.time())
    timestr = str(timestamp)
    accesstoken = getAccesstoken()
    wxticket = getJsApiTicket(accesstoken)
    wxnoncestr = "trailblazers"
    
    tmpstr = "jsapi_ticket=%s&noncestr=%s&timestamp=%s&url=%s" %(wxticket,wxnoncestr,timestr,url)
    hashstr = hashlib.sha1(tmpstr).hexdigest()

    return {'signature':hashstr, 'nonceStr':wxnoncestr, 'timestamp':timestr}
