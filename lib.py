# -*- coding: cp936 -*-
import time
import urllib2
import json
from xml.etree import ElementTree
def xmlParse(data):
    req = ElementTree.fromstring(data)
    ToUserName = req.find('ToUserName').text
    FromUserName = req.find('FromUserName').text
    Content = req.find('Content').text
    res = '<xml><ToUserName><![CDATA[%s]]></ToUserName>' +\
    '<FromUserName><![CDATA[%s]]></FromUserName>' +\
    '<CreateTime>%s</CreateTime>' +\
    '<MsgType><![CDATA[text]]></MsgType>' +\
    '<Content><![CDATA[%s]]></Content>' +\
    '<FuncFlag>0</FuncFlag></xml>'
    Content = translation(Content)
    res = res % (FromUserName, ToUserName, str(int(time.time())), Content)
    return res

def translation(req):
    ans = ''
    url = 'http://fanyi.youdao.com/openapi.do?keyfrom=Your_keyfrom' +\
    '&key=Your_key&type=data&doctype=json&version=1.1&q=' + req
    text = urllib2.urlopen(url).read()
    res = json.loads(text)
    if res["errorCode"] == 0:
        if res["translation"][0] == req:
            ans = ans + "wu :("
        else:
            ans = ans + res["translation"][0]
    return ans
