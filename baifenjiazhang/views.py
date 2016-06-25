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
                xml = wechat.response_text(content = u"后台功能升级中...")
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
        elif isinstance(wechat.message, TextMessage):
            xml = wechat.response_text(content = u"对不起，暂不支持该功能")
        elif wechat.message.type == 'click':
            xml = wechat.response_text(content = u"点击事件key = [%s]" % wechat.message.key)
        # 关注事件
        elif wechat.message.type == 'subscribe':
            message = u'''感谢关注百分家长，我们专注于帮助家长提高孩子的成绩。为此我们会不定期分享学习资料，每周四安排一位专家老师教育知识和学习方法。\n回复 期末 下载最新的期末试卷\n\n消息自动回复：\n这里自动回复，下载期末试卷请回复 期末\n已经得到下载链接，但是不会下载，请回复 下载'''
            xml = wechat.response_text(content = message)
        else:
            xml = wechat.response_text(content = u"对不起，暂不支持该功能")
        return HttpResponse(xml, content_type = "application/xml")
