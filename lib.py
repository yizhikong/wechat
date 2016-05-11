# coding: UTF-8
import time
import urllib
import urllib2
import sys
#import dbHandler
import json
import hashlib
from xml.etree import ElementTree
from values import *
import redis
import ImgProcess
import cv2
import re

# has key "username_originImgName", "username_status" and "username_setting"
redis_client = redis.StrictRedis(host = 'localhost', port = 6379, db = 0)

def xmlParse(data):
    req = ElementTree.fromstring(data)
    xml = {}
    xml['ToUserName'] = req.find('ToUserName').text
    xml['FromUserName'] = req.find('FromUserName').text
    xml['MsgType'] = req.find('MsgType').text
    if xml['MsgType'] == "event":
        return dueEvent(xml, req)
    elif xml['MsgType'] == "text":
        return dueText(xml, req)
    else:
        return dueImage(xml, req)
    
def dueEvent(xml, req):
    Event = req.find('Event').text
    if Event == "subscribe":
        response = res % (xml['FromUserName'], xml['ToUserName'], str(int(time.time())), welcome)
        #dbHandler.createTable(encode(xml['FromUserName']))
        return response
    elif Event == "unsubscribe":
        #dbHandler.dropTable(encode(xml['FromUserName']))
        pass
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
    print 'due Text'
    createTime = str(int(time.time()))
    try:
        Content = req.find('Content').text
        # ============================ image process ============================
        if "setting" in Content:
            pat = re.compile("\d+")
            height, width = pat.findall(Content)
            redis_client.set(xml["FromUserName"] + "_setting", height + "_" + width)
            return res % (xml['FromUserName'], xml['ToUserName'], str(int(time.time())), 'Change setting success!')

        if redis_client.get(xml["FromUserName"] + "_status") == "selecting":
            # get select numbers
            pat = re.compile("\d+")
            select = map(lambda x : int(x), pat.findall(Content))
            # get original image name in redis and process
            redis_key = xml["FromUserName"] + "_originImgName"
            originImgName = redis_client.get(redis_key)
            height, width = 2, 3
            if redis_client.exists(xml["FromUserName"] + "_setting"):
                setting = redis_client.get(xml["FromUserName"] + "_setting")
                height = int(setting.split('_')[0])
                width = int(setting.split('_')[1])
            img = cv2.imread("static/" + originImgName)
            for s in select:
                img = ImgProcess.process(img, s, width, height)
            # save result
            resultImgName = xml["FromUserName"] + createTime + '_result.jpg'
            cv2.imwrite('static/' + resultImgName, img)
            # return
            url = imgRoot + resultImgName
            redis_client.set(xml["FromUserName"] + "_status", "")
            return linkRes % (xml['FromUserName'], xml['ToUserName'], createTime, 'Result', 'Thanks!', url, url)

        # ============================ special process ============================
		# some special response
        if Content in dic:
            return res % (xml['FromUserName'], xml['ToUserName'], str(int(time.time())), dic[Content])
        # url jump response, to show the article
        if Content in jdic:
            return jump % (xml['FromUserName'], xml['ToUserName'], str(int(time.time())), tdic[Content], '', '', jdic[Content])

        # ============================ translation process ============================
        Content = translation(Content, xml['FromUserName'])
    except:
        Content = "Exception!"
    response = res % (xml['FromUserName'], xml['ToUserName'], str(int(time.time())), Content)
    return response

def dueImage(xml, req):
    createTime = str(int(time.time()))
    try:
        # get user's photo url
        PicUrl = req.find('PicUrl').text
        img = urllib2.urlopen(PicUrl).read()
        # set user's original photo name in redis
        originImgName = xml["FromUserName"] + "_" + createTime + "_temp.jpg"
        redis_key = xml["FromUserName"] + "_originImgName"
        redis_client.set(redis_key, originImgName)
        # save user's photo in ali cloud with the original image name in redis
        f = open("static/" + originImgName, "w")
        f.write(img)
        f.close()
        # read the origin photo with opencv and process
        img = cv2.imread("static/" + originImgName)
        height, width = 2, 3
        if redis_client.exists(xml["FromUserName"] + "_setting"):
            setting = redis_client.get(xml["FromUserName"] + "_setting")
            height = int(setting.split('_')[0])
            width = int(setting.split('_')[1])
        cropimg = ImgProcess.getBlockImg(img, width, height)
        # save the block image in ali cloud and set the redis
        blockImgName = xml["FromUserName"] + "_" + createTime + "_block.jpg"
        cv2.imwrite('static/' + blockImgName, cropimg)
        redis_client.set(xml["FromUserName"] + "_status", "selecting")
        # create image url and return
        url = imgRoot + blockImgName
        response = linkRes % (xml['FromUserName'], xml['ToUserName'], createTime, 'Please reply numbers to process', 'for example: 0,3', url, url)
        return response
    except:
        return res % (xml['FromUserName'], xml['ToUserName'], str(int(time.time())), 'Fail')

# translate(English, Janpanse and so on -> Chinese, Chinese -> English), use youdao API
def translation(Content, FromUserName):
    req = Content
    if type(req).__name__ == 'unicode':
        req = req.encode('UTF-8')
        req = urllib2.quote(req)
    else:
        #dbHandler.insertWord(encode(FromUserName), Content)
        pass
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

