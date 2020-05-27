import time
import hmac
import hashlib
import base64
import urllib.parse
import requests
import sys
import os
args=sys.argv
# https://oapi.dingtalk.com/robot/send?access_token=3215c9f1db64af0dd36f0ead362a6e1efa396e5f0a5d16c3bae96a7f54fcf1c3
timestamp = str(round(time.time() * 1000))
secret = 'SEC2ccd2ddab62cf3fab49abe53851aafbc5480ad5b6803c622b2d5edfbb78a9546'
secret_enc = secret.encode('utf-8')
string_to_sign = '{}\n{}'.format(timestamp, secret)
string_to_sign_enc = string_to_sign.encode('utf-8')
hmac_code = hmac.new(secret_enc, string_to_sign_enc,
                     digestmod=hashlib.sha256).digest()
sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

path = os.path.abspath(os.path.curdir)+"/bin/targets"
if os.path.exists(path):
    files = os.listdir(path)
    has = False
    for file in files:
        if file.count("sha256sums")>0:
            has = True
        if file.count("rpi-3")>0:
            has = True
    if has:
        content="编译成功"
    else:
        content="编译失败"
else:
    content="编译失败"


url =args[1] +"&timestamp=%s&sign=%s" % (
    timestamp, sign
)
headers = {"Content-Type":"application/json;charset=utf-8"}
data = {
    "msgtype": "text",
    "text": {"content": content}
}
r=requests.post(url=url, json=data,headers=headers)
print(r.text)
