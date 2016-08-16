# -*- coding: utf-8 -*-
__author__: 'Kyliiat'
import requests, re
from bs4 import BeautifulSoup
import http.cookiejar
import base64, json, rsa, os, time, random, datetime, binascii
import urllib.parse

# jr m.version
html = requests.session()
list = []

headers_={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Connection': 'keep-alive',
}
headers1={
    'Host': 'passport.weibo.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F',
    'Content-Length': '236',
    'Connection': 'keep-alive',
}

headers_l={
'Host': 'm.weibo.cn',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0',
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding': 'gzip, deflate',
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'X-Requested-With': 'XMLHttpRequest',
'Referer': 'http://m.weibo.cn/',
'Content-Length': '34',
'Connection': 'keep-alive',
}

data_={
    'username': '',
    'password': '',
    'savestate': '1',
    'ec': '0',
    'pagerefer': 'http%3A%2F%2Fpassport.sina.cn%2Fsso%2Flogout%3Fentry%3Dmweibo%26r%3Dhttp%253A%252F%252Fm.weibo.cn',
    'entry': 'mweibo',
    'wentry': '',
    'loginfrom': '',
    'client_id': '',
    'code': '',
    'qq': '',
    'hff': '',
    'hfp': '',
}

like_data={
    'id': '',
    'attitude': 'heart',
}

#login
username = input('username: ')
password = input('password: ')
data_['username'] = username
data_['password'] = password

like_url = 'http://m.weibo.cn/attitudesDeal/add'
url = 'https://login.sina.com.cn/sso/prelogin.php?checkpin=1&entry=mweibo&su=Yml1Yml1MDklNDAxMjYuY29t&callback=jsonpcallback1467307433925'
try:
    r0 = html.get(url, headers=headers_)
    print('get #1, ok')
except:
    print('get #1 failed')

url_pass = 'https://passport.weibo.cn/sso/login'
try:
    r1 = html.post(url_pass, headers=headers1, data=data_)
    print('login, ok')
except:
    print('login failed')

uid = input('uid: ')

try:
    r2 = html.get('http://m.weibo.cn', headers=headers_)
    print('get #2, ok')
except:
    print('get #2, failed')

filename = uid + '.txt'   # 文件以uid.txt命名, 里面存mid列表
if os.path.exists(filename):     # 文件存在, 先读入更新列表
    file = open(filename, 'r+')
    while True:
        line = ''
        line = file.readline()
        if line != '':
            line = line.rstrip()
            list.append(line)
        else:
            break
else:                           # 文件不存在, 创建新文件
    file = open(filename, 'w')

def loop():
    r2 = html.get('http://m.weibo.cn/index/feed?format=cards', headers=headers_)
    a = r2.json()

    # deal with json package
    for item in a[0]['card_group']:
        if str(item['mblog']['user']['id']) == uid:
            mid = item['mblog']['mid']
            if mid not in list:
                list.append(mid)
                file.write(mid + '\n')
                like_data['id'] = mid
                rr = html.post(like_url, headers=headers_l, data=like_data)
                print('like:', item['mblog']['mid'])


while True:
    try:
        loop()
    except:
        print('loop, failed')
    time.sleep(10)

