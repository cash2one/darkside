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
            xml = wechat.response_text(content = u"后台功能升级中...")
        # 关注事件
        # elif wechat.message.type == 'subscribe':
        #     help_string = [{
        #         "title": "公众号使用帮助",
        #         "url": "http://mp.weixin.qq.com/s?__biz=MzI1OTMwMzkxNw==&mid=100000045&idx=1&sn=09e37fbb835f004a4a4d5eaaabb59187#rd",
        #         "picurl": "https://mmbiz.qlogo.cn/mmbiz/CicuwT5KbSicKoq42aPGibicF7XJPibfyqbp0jiania2PiaFF5LywMbLwO7SQlddJOFcMLmNmQM1KXvQu5lGx8jgbXkE7Q/0?wx_fmt=jpeg",
        #     }]
        #     xml = wechat.response_news(help_string)
        else:
            xml = wechat.response_text(content = u"对不起，暂不支持该功能")
        return HttpResponse(xml, content_type = "application/xml")
