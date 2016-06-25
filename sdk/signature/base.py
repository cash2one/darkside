#!/usr/bin/env python
#-*- coding:utf-8 -*-
import hashlib

class Signature(object):
    @staticmethod
    def check_signature(request, token):
        signature = request.GET.get("signature")
        timestamp = request.GET.get("timestamp")
        nonce = request.GET.get("nonce")

        tmparr = [token, timestamp, nonce]
        tmparr.sort()
        encode = hashlib.sha1("".join(tmparr)).hexdigest()
        if encode == signature:
            return True
        else:
            return False
