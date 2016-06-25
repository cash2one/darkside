#!/usr/bin/env python
import requests
import urllib
import urllib2

url = "http://www.genshuixue.com/i-api/weixin/tags.post"

post_data = urllib.urlencode({"_ticket": "yueqiubeimianyouyituodoufuzha"})
req = urllib2.urlopen(url, post_data)
print req.read()
