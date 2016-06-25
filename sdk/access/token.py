#-*- coding:utf-8 -*-
import urllib
import time
import json

def get_access_token(base, appid, secret):
    current_time = int(time.time())
    expire = base.get("expire", 0)
    if current_time > expire:
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appid, secret)
        try:
            response = json.JSONDecoder().decode(urllib.urlopen(url).read())
            return {
                "access_token": response.get("access_token"),
                "expire": current_time + 7000
            }
        except:
            return base
    return base
