# -*- coding: utf-8 -*-

import json
import time
import urllib.request
import hashlib

def sign(appSecret, content):
    """签名"""
    s = appSecret + 'AppKey' + content['appKey'] + 'Data' + content['data'] + 'Timestamp' + str(content['timestamp']) + appSecret
    m = hashlib.md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()

class OpenClient():


    """open sdk client"""
    def __init__(self, appKey, appSecret, url):
        self.url = url
        self.appKey = appKey
        self.appSecret = appSecret

    def executeSign(self, request):
        """执行请求"""
        a = self.appKey
        content = {
            'appKey': a,
            'data': json.dumps(request.__dict__),
            'timestamp': int(time.time())
        }
        content['sign'] = sign(self.appSecret, content)
        u = self.url + '/' + request.getApiMethod()
        params = json.dumps(content).encode('utf-8')
        headers = { 'content-type': 'application/json' }
        req = urllib.request.Request(url=u, data=params, headers=headers, method='POST')
        response = urllib.request.urlopen(req).read().decode()
        return json.loads(response)