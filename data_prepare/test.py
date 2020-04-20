# -*- coding:utf-8 -*-
"""
author: byangg
datettime: 2020/4/20 14:10
"""
import json

import requests

corpid = ""
corpsecret = ""
headers = {
    "Content-Type": "application/json; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
}

target_url = "localhost:1324/wechat"

# 判断是否登录，跳转
# 未登录
url_unlogin = f"https://open.weixin.qq.com/connect/oauth2/authorize?appid={corpid}&redirect_uri={target_url}" \
             "&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect"
# "localhost:1324/wechat?code=CODE&state=STATE

CODE = ''

url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}"
response = requests.post(url, headers=headers).text
ACCESS_TOKEN = json.loads(response)['access_token']

user_url = f"https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token={ACCESS_TOKEN}&code={CODE}"
response = requests.post(url, headers=headers).text
username = json.loads(response)['UserId']

# GET
# https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ID&corpsecret=SECRET
# {
#    "errcode": 0,
#    "errmsg": "ok",
#    "access_token": "accesstoken000001",
#    "expires_in": 7200
# }

# https://open.weixin.qq.com/connect/oauth2/authorize?appid=CORPID&redirect_uri=REDIRECT_URI&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect
# 假定当前
# 企业CorpID：wxCorpId
# 访问链接：http://api.3dept.com/cgi-bin/query?action=get
# 根据URL规范，将上述参数分别进行UrlEncode，得到拼接的OAuth2链接为：
# https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxCorpId&redirect_uri=http%3a%2f%2fapi.3dept.com%2fcgi-bin%2fquery%3faction%3dget&response_type=code&scope=snsapi_base&state=#wechat_redirect
# 员工点击后，页面将跳转至
# http://api.3dept.com/cgi-bin/query?action=get&code=AAAAAAgG333qs9EdaPbCAP1VaOrjuNkiAZHTWgaWsZQ&state=
# 企业可根据code参数调用获得员工的userid


# https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=ACCESS_TOKEN&code=CODE
# {
#    "errcode": 0,
#    "errmsg": "ok",
#    "UserId":"USERID",
#    "DeviceId":"DEVICEID"
# }

headers = {
    "Content-Type": "application/json; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
}

url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}"
response = requests.post(url, headers=headers).text
token = json.loads(response)['access_token']



# 1、 未登陆 跳转：

# https://open.weixin.qq.com/connect/oauth2/authorize?appid=配置文件corpid&redirect_uri=https://cloud.lk-cl.com:8443/appraisal/接收CODE页面&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect

# 腾讯会跳转回来 https://cloud.lk-cl.com:8443/appraisal/接收CODE页面?code=CODE&state=STATE
# 再请求  获取 token
# https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=配置文件corpid&corpsecret=配置文件secret
#
# 返回结果：
# {
#    "errcode": 0,
#    "errmsg": "ok",
#    "access_token": "accesstoken000001",
#    "expires_in": 7200
# }
# 最后根据CODE 获取用户信息
# https://qyapi.weixin.qq.com/cgi-bin/user/getuserinfo?access_token=ACCESS_TOKEN&code=CODE
# 返回结果：
# a) 当用户为企业成员时返回示例如下：
# {
#    "errcode": 0,
#    "errmsg": "ok",
#    "UserId":"USERID",
#    "DeviceId":"DEVICEID"
# }