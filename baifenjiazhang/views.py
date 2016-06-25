#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.messages import TextMessage, ImageMessage
import json
import urllib
import urllib2

# Create your views here.

wechat_conf = WechatConf(
    token = "baifenjiazhang_genshuixue",
    appid = "wx607fb967a5b52ae9",
    appsecret = "13a74f10843bb3b316c88f2a1e1f764b",
    encrypt_mode = "normal",
    encoding_aes_key = "rBSkOY8YVTR5PBlyCrhuR7Ll1qgvi2fiIk2hkTY1JWk"
)

wechat = WechatBasic(conf = wechat_conf)
zhanqun_weixin_url = "http://www.genshuixue.com/i-api/weixin/tags.post"

@csrf_exempt
def home(request):
    signature = request.GET.get("signature")
    timestamp = request.GET.get("timestamp")
    nonce = request.GET.get("nonce")
    if request.method == "GET":
        if wechat.check_signature(signature, timestamp, nonce):
            return HttpResponse(request.GET.get("echostr"))
        return HttpResponse("forbidden.")
    elif request.method == "POST":
        wechat.parse_data(request.body)
        data = {"_ticket": "yueqiubeimianyouyituodoufuzha",
                "wechat_id": wechat.message.id,          # 对应于 XML 中的 MsgId
                "wechat_target": wechat.message.target,  # 对应于 XML 中的 ToUserName
                "wechat_source": wechat.message.source,  # 对应于 XML 中的 FromUserName
                "wechat_time": wechat.message.time,      # 对应于 XML 中的 CreateTime
                "wechat_type": wechat.message.type,      # 对应于 XML 中的 MsgType
                "wechat_raw": wechat.message.raw,        # 原始 XML 文本，方便进行其他分析
                }
        if isinstance(wechat.message, TextMessage):
            if wechat.message.content and wechat.message.content.startswith(u"@小黄鸡 "):
                ret = json.JSONDecoder().decode(urllib.urlopen("http://api.simsimi.com/request.p?key=yourkey&lc=zh&ft=1.0&text=%s" % urllib.quote(wechat.message.content.split(" ", 1)[1].encode("utf-8"))).read())
                xml = wechat.response_text(ret.get("response", "I don't understand what you say ~~~"))
            else:
                if wechat.message.content == u"期末":
                    message = u'''这次试卷整理的比较全，希望能帮助更多的家长，希望大家多多传递。按照以下操作领取试卷\n''' +\
                              u'''第一步：转发下面的图片到朋友圈，并配上下面这句话：\n小学1-5年级期末复习时间，考前提分冲刺，扫描领取，推荐给大家。<a href="http://mp.weixin.qq.com/s?__biz=MzA5MjQ2ODgzMA==&mid=503512941&idx=1&sn=a7c316a9780554d3bc27f21b27a9376c#rd">点击获取图片</a>\n第二步：分享后截图，并将截图发给百分家长公众号。\n''' +\
                              u'''符合条件的家长将收到下载链接，不然有会被拉黑，永远收不到之后的资料了哟'''
                    xml = wechat.response_text(content = message)
                    # xml += wechat.response_image(media_id = "pqn1KlnugZbvRsXJ3aW5Z3OUfJqetQ66R8ggDdkOKbY")
                elif wechat.message.content == u"下载":
                    message = u'''下载遇到问题请点击<a href="http://mp.weixin.qq.com/s?__biz=MzA5MjQ2ODgzMA==&mid=503512906&idx=1&sn=610ac39498936cdc5dea38a532dfb4f1#rd">这里</a>'''
                    xml = wechat.response_text(content = message)
                elif wechat.message.content == u"密码":
                    message = u'''cixn，链接后面已经告知密码了，请您细心一点哟'''
                    xml = wechat.response_text(content = message)
                elif wechat.message.content == u"图片":
                    xml = wechat.response_image(media_id = "pqn1KlnugZbvRsXJ3aW5Z3OUfJqetQ66R8ggDdkOKbY")
                else:
                    xml = wechat.response_text(content = u'''不支持当前查询''')
                # data["wechat_content"] = wechat.message.content.encode("utf-8")
                # post_data = urllib.urlencode(data)
                # req = json.JSONDecoder().decode(urllib2.urlopen(zhanqun_weixin_url, post_data).read())
                # if int(req["code"]) == 0:
                #     if req["type"] == "text":
                #         xml = wechat.response_text(content = req["msg"])
                #     elif req["type"] == "image":
                #         xml = wechat.response_text(content = "image")
                #     elif req["type"] == "news":
                #         xml = wechat.response_news(req["msg"])
                # else:
                #     xml = wechat.response_text(req.get("msg", wechat.message.content))
        elif isinstance(wechat.message, ImageMessage):
            message = u'''期末试卷下载链接: http://pan.baidu.com/s/1miRKcw4 密码: cixn\n''' +\
                      u'''没有注册云盘的记得先注册，直接点开地址一键保存到自己的云盘，保存好就可以慢慢下载啦！因太多朋友下载，出现无法打开的现象，请耐心等待。不懂如何下载的朋友可以回复关键词：下载'''
            xml = wechat.response_text(content = message)
        elif wechat.message.type == 'click':
            if wechat.message.key == u"期末":
                message = u'''这次试卷整理的比较全，希望能帮助更多的家长，希望大家多多传递。按照以下操作领取试卷\n''' +\
                          u'''第一步：转发下面的图片到朋友圈，并配上下面这句话：\n小学1-5年级期末复习时间，考前提分冲刺，扫描领取，推荐给大家。<a href="http://mp.weixin.qq.com/s?__biz=MzA5MjQ2ODgzMA==&mid=503512941&idx=1&sn=a7c316a9780554d3bc27f21b27a9376c#rd">点击获取图片</a>\n第二步：分享后截图，并将截图发给百分家长公众号。\n''' +\
                          u'''符合条件的家长将收到下载链接，不然有会被拉黑，永远收不到之后的资料了哟'''
                xml = wechat.response_text(content = message)
        # 关注事件
        elif wechat.message.type == 'subscribe':
            message = u'''感谢关注百分家长，我们专注于帮助家长提高孩子的成绩。为此我们会不定期分享学习资料，每周四安排一位专家老师教育知识和学习方法。\n回复 期末 下载最新的期末试卷'''
            xml = wechat.response_text(content = message)
        else:
            xml = wechat.response_text(content = u"对不起，暂不支持该功能")
        return HttpResponse(xml, content_type = "application/xml")
