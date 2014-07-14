# coding: UTF-8
# ___________________________________________________________________________

#     Attention! All of these should be in database! I am too lazy so...

# ___________________________________________________________________________

res = '<xml><ToUserName><![CDATA[%s]]></ToUserName>' +\
'<FromUserName><![CDATA[%s]]></FromUserName>' +\
'<CreateTime>%s</CreateTime>' +\
'<MsgType><![CDATA[text]]></MsgType>' +\
'<Content><![CDATA[%s]]></Content>' +\
'<FuncFlag>0</FuncFlag></xml>'

welcome = u"欢迎关注yzkk\'s cat o>_<o！~\n本订阅号的主要功能为翻译（也是默认功能），\n另还会分享一些有趣的东西哦\n回复#help可以获取全部功能"
jump = '<xml><ToUserName><![CDATA[%s]]></ToUserName>' +\
'<FromUserName><![CDATA[%s]]></FromUserName>' +\
'<CreateTime>%s</CreateTime>' +\
'<MsgType><![CDATA[news]]></MsgType>' +\
'<ArticleCount>1</ArticleCount>' +\
'<Articles>'+\
'<item> '+\
'<Title><![CDATA[%s]]></Title>' +\
'<Description><![CDATA[%s]]></Description>' +\
'<PicUrl><![CDATA[%s]]></PicUrl>' +\
'<Url><![CDATA[%s]]></Url>' +\
'</item>' +\
'</Articles>' +\
'</xml>' 

APPID = 'YOURAPPID'
APPSECRET ='YOURAPPSECRET'
accessTokenAPI = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'
translationAPI = 'http://fanyi.youdao.com/openapi.do?keyfrom=yzkkCat&key=686375979&type=data&doctype=json&version=1.1&q='
openIdAPI = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'
sendMsgAPI = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token='
createMenuAPI = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token='
deleteMenuAPI = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token='
articleList = 'http://mp.weixin.qq.com/s?__biz=MzA4MzM4MDYwOQ==&mid=200604976&idx=1&sn=4037906038946a1278a323df8ed3281d#rd'
aboutMeUrl = 'http://mp.weixin.qq.com/s?__biz=MzA4MzM4MDYwOQ==&mid=200604998&idx=1&sn=d3c3e4a5f98b1bec0c8f9c0f7e2e4de7#rd'
redirect_uri = 'yzkk.sinaapp.com/test'
keyOfTucao = 'KeyOfTuCao'

# special response:)
dic = {}
dic[u"翼之空空"] = u"主人的网名哦~"
# ...........
# ...........
# add as you like
# ...........
# ...........
dic[u"聊天"] = u"猫猫还只会说几句话啦" 
dic[u"yzkk's cat"] = u"我才不是yzkk的>_<" 
dic[u"我恨你"] = u"呜呜"
dic[u"好厉害"] = u"主人教我讲话的啦~"
dic[u"好可爱"] = u"喵喵~"
dic[u"猫"] = u"喵呜~"
dic[u"喵"] = u"喵?"
dic[u"#help"] = u'【操作提示】：\n1.本订阅号默认功能是翻译，支持英译中，日译中，法译中，中译英等\n' +\
u'2.回复#list words 可以获取自己以前查阅过的单词，以便检验自己查阅后是否还能记住\n' +\
u'3.回复#list可获取分享的文章列表\n' +\
u'4.回复个别短语或许会有特殊回复\n' +\
u'5.回复#help可以获取此帮助菜单\n' +\
u'6.发现bug请与我联系'
dic[u"#list"] = u"【文章列表】\n1.周易简介\n2.【最终篇】占卦与解卦\n3.皮皮虾能以子弹出膛速度出击捕食？\n4.为什么诈骗短信看上去那么弱智？" +\
u"【搬运】\n5.中国古代传说中有哪些鬼怪？\n6.拍照会降低亲身的体验吗？\n\n回复#加文章序号即可获取文章，如#3"

# urls of article, be related to tdic{}
jdic = {}
jdic["#1"] = 'http://mp.weixin.qq.com/s?__biz=MzA4MzM4MDYwOQ==&mid=200088029&idx=1&sn=2df11a4ed3c088eb10fe1b1ea637ce9e#rd'
jdic["#2"] = 'http://mp.weixin.qq.com/s?__biz=MzA4MzM4MDYwOQ==&mid=200161888&idx=1&sn=b93c4d4c6818f6666cab9b9ddb0ae338#rd'
jdic["#3"] = 'http://mp.weixin.qq.com/s?__biz=MzA4MzM4MDYwOQ==&mid=200103413&idx=1&sn=909d5327b5718f53dfe8b23c2b918b49#rd'
jdic["#4"] = 'http://mp.weixin.qq.com/s?__biz=MzA4MzM4MDYwOQ==&mid=200202050&idx=1&sn=65a833bd8a641e1e7c9647d0b101d2e9#rd'
jdic["#5"] = 'http://mp.weixin.qq.com/s?__biz=MzA4MzM4MDYwOQ==&mid=200271317&idx=1&sn=50c15391ab896017992acb2866615ca5#rd'
jdic["#6"] = 'http://mp.weixin.qq.com/s?__biz=MzA4MzM4MDYwOQ==&mid=200413546&idx=1&sn=0583f06073c7b5c4c38352e7224457da#rd'

# titles of article, be related to tdic{}
tdic = {}
tdic["#1"] = u"周易简介"
tdic["#2"] = u"【最终篇】占卦与解卦"
tdic["#3"] = u"皮皮虾能以子弹出膛速度出击捕食？"
tdic["#4"] = u"为什么诈骗短信看上去那么弱智？【搬运】"
tdic["#5"] = u"中国古代传说中有哪些鬼怪？"
tdic["#6"] = u"拍照会降低亲身的体验吗？"

