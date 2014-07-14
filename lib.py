# coding: UTF-8
import time
import urllib
import urllib2
import sys
import dbHandler
import json
import hashlib
from xml.etree import ElementTree
from values import *

def xmlParse(data):
    req = ElementTree.fromstring(data)
    xml = {}
    xml['ToUserName'] = req.find('ToUserName').text
    xml['FromUserName'] = req.find('FromUserName').text
    xml['MsgType'] = req.find('MsgType').text
    if xml['MsgType'] == "event":
        return dueEvent(xml, req)
    else:
        return dueText(xml, req)
    
def dueEvent(xml, req):
    Event = req.find('Event').text
    if Event == "subscribe":
        response = res % (xml['FromUserName'], xml['ToUserName'], str(int(time.time())), welcome)
        dbHandler.createTable(encode(xml['FromUserName']))
        return response
    elif Event == "unsubscribe":
        dbHandler.dropTable(encode(xml['FromUserName']))
    elif Event == "CLICK":
        key = req.find('EventKey').text
        if key == keyOfTucao:
            Content = u"本订阅号暂不提供吐嘈功能=。="
            response = res % (xml['FromUserName'], xml['ToUserName'], str(int(time.time())), Content)
            return response
    else:
        response = res % (xml['FromUserName'], xml['ToUserName'], str(int(time.time())), Event)
        return response

def dueText(xml, req):
    try:
        Content = req.find('Content').text
		# this response is related to database. So I list it here.
        if Content == "list words" or Content == "#list words":
            Content = "\n".join(dbHandler.listWords(encode(xml['FromUserName'])))
        elif Content is None:
            Content = "no word"
        else:
			# some special response
            if Content in dic:
                response = res % (xml['FromUserName'], xml['ToUserName'], str(int(time.time())), dic[Content])
                return response
            # url jump response, to show the article
            if Content in jdic:
                response = jump % (xml['FromUserName'], xml['ToUserName'], str(int(time.time())), tdic[Content], '', '', jdic[Content])
                return response
            # translation part 
            Content = translation(Content, xml['FromUserName'])
    except:
        Content = "Exception!"
    response = res % (xml['FromUserName'], xml['ToUserName'], str(int(time.time())), Content)
    return response

# translate(English, Janpanse and so on -> Chinese, Chinese -> English), use youdao API
def translation(Content, FromUserName):
    req = Content
    if type(req).__name__ == 'unicode':
        req = req.encode('UTF-8')
        req = urllib2.quote(req)
    else:
        dbHandler.insertWord(encode(FromUserName), Content)
    word = ''
    url = translationAPI + req
    text = urllib2.urlopen(url).read()
    res = json.loads(text)
    if res["errorCode"] == 0:
        if 'basic' in res.keys():
            word = '[' + Content + ']'
            for ex in res["basic"]["explains"]:
                word = word + '\n ' + ex
        else:
            word = '[' + Content + ']\n  ' + res["translation"][0]
    else:
        word = word + ":("
    return word

# get openId. Only can be used by service account or test account
def getOpenId(code):
    openUrl = openIdAPI % (APPID, APPSECRET, code)
    text = urllib2.urlopen(openUrl).read()
    res = json.loads(text)
    openid = res['openid']
    send(openid)

# get accesstoken. Only can be used by service account or test account
def getAccessToken():
    aturl = accessTokenAPI % (APPID, APPSECRET)
    atreq = urllib2.Request(aturl)
    atres = urllib2.urlopen(atreq)
    at = atres.read()
    accessToken = (json.loads(at))["access_token"]
    return accessToken

# send message to users. Only can be used by service account or test account
def send(openid):
    accessToken = getAccessToken()
    #print "accessToken is " + accessToken
    data = {"touser" : openid,
            "msgtype" : "text",
            "text" : {"content" : "hello world"}
            }
    urlData = urllib.urlencode(data)
    url = sendMsgAPI + accessToken
    req = urllib2.Request(url = url, data = urlData)
    #print req
    return urllib2.urlopen(req).read()
    #print res

# create menu. Only can be used by service account or test account. Or subscribe account which has dealt with authentication
def createMenu():
    accessToken = getAccessToken()
    #print "accessToken is " + accessToken
    data = '''{"button" : [
                        {
                         "type" : "view",
                         "name" : "文章目录",
                         "url" : "%s"
                         },
                        {
                         "name" : "联系wo",
                         "sub_button" : [
                                         {
                                          "type" : "view",
                                          "name" : "关于我",
                                          "url" : "%s"
                                          },
                                         {
                                          "type" : "click",
                                          "name" : "吐嘈我",
                                          "key" : "tucao"
                                          }]
                         }]
            }''' % (articleList, aboutMeUrl)
    #urlData = urllib.urlencode(data)
    #urlData = json.JSONEncoder(ensure_ascii = False).encode(data)
    url = createMenuAPI + accessToken
    req = urllib2.Request(url = url, data = data)
    return urllib2.urlopen(req).read()

# delete menu. Only can be used by service account or test account. Or subscribe account which has dealt with authentication
def deleteMenu():
    accessToken = getAccessToken()
    res = urllib2.urlopen(deleteMenuAPI + accessToken)
    return res.read()


# encode the username, create database table(store the words)
def encode(username):
    code = hashlib.md5(username)
    return code.hexdigest()

