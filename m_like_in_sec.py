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
    'pcid': '',
    'pincode': '',
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

cmt_data={
    'content': '',
    'id': '',
    'st': '',
}

username = input('username: ')
password = input('password: ')
data_['username'] = username
data_['password'] = password

like_url = 'http://m.weibo.cn/attitudesDeal/add'
cmt_url = 'http://m.weibo.cn/commentDeal/addCmt'
init_url = 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http://m.weibo.cn/'

rr = html.get(init_url, headers=headers_)

# get pincode and pcid
url_image = 'https://passport.weibo.cn/captcha/image'
ra = html.get(url_image)
rj = ra.json()
data_['pcid'] = rj['data']['pcid']
print(ra.text)
data_['pincode'] = input('pincode: ')

# login
url_pass = 'https://passport.weibo.cn/sso/login'
r1 = html.post(url_pass, headers=headers1, data=data_)
print(r1.text)

uid = input('uid: ')

# collect st and content
st_f = ''

cmt_data['content'] = input('comment: ')
try:
    r2 = html.get('http://m.weibo.cn', headers=headers_)
    st_f = re.findall(r'(?<=\"st\":\")[0-9]+(?=\")', r2.text)
    # print('st:' + st_f[0])
    print('get #2, ok')
except:
    print('get #2, failed')
cmt_data['st'] = st_f


filename = uid + '_cmt.txt'   # 文件以uid.txt命名, 里面存mid列表
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
    # print(a)
    # deal with json package
    for item in a[0]['card_group']:
        if str(item['mblog']['user']['id']) == uid:
            mid = item['mblog']['mid']
            if mid not in list:
                list.append(mid)
                file.write(mid + '\n')
                like_data['id'] = mid
                cmt_data['id'] = mid
                comnt = html.post(cmt_url, headers=headers_l, data=cmt_data)  # post comment
                print('post comment, done')
                exit(0)
                rr = html.post(like_url, headers=headers_l, data=like_data)  # post heart
                # print('like:', item['mblog']['mid'])


while True:
    try:
        loop()
    except:
        print('loop failed')
    time.sleep(10)

