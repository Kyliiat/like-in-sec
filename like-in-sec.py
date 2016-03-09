# -*- coding: utf-8 -*-
import requests, re
from bs4 import BeautifulSoup
import http.cookiejar
import base64, json, rsa, os, time, random, datetime, binascii
import urllib.parse

html = requests.session()

username = input('输入用户名/邮箱/电话号码: ')
password = input('输入密码: ')
list = []
ouid = ''
my_id = ''

publickey = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB\
784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
pubkey = int(publickey, 16)

# 待取得的有su, servertime, nonce, sp 四个
postdata = {
    'entry':'weibo',
    'gateway':'1',
    'from':'',
    'savestate':'7',
    'useticket':'1',
    'pagerefer':'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F',
    'vsnf':'1',
    'su':'',
    'service':'miniblog',
    'servertime':'',
    'nonce':'',
    'pwencode':'rsa2',
    'rsakv':'1330428213',
    'sp':'',
    'sr':'1920*1080',
    'encoding':'UTF-8',
    'prelt':'67',
    'url':'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
    'returntype':'META',
}

headers_ = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0',
}

like_data={
    'location': 'v6_content_home',
    'group_source': 'group_all',
    'rid': '',
    'version': 'mini',
    'qid': 'heart',
    'mid': '',
    'like_src': '1',
}
like_url = 'http://www.weibo.com/aj/v6/like/add?ajwvr=6'

def get_sp(servertime, nonce):
    key = rsa.PublicKey(pubkey, 65537)
    message=str(servertime) + '\t' + str(nonce) + '\n' + password
    sp=rsa.encrypt(message.encode(), key)
    sp=binascii.b2a_hex(sp)
    return sp.decode('utf-8')

def get_su():
    string = urllib.parse.quote(username)
    return base64.b64encode(string.encode()).decode('utf-8')

def get_servertime():  # and nonce
    url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&su=%s&checkpin=1&rsakt=mod' % (get_su())
    page = html.get(url)
    data = json.loads(page.text)
    # print(data)
    result = []
    result.append(str(data['servertime']))
    result.append(str(data['nonce']))
    result.append(str(data['pcid']))
    return result

def login():
    su = get_su()
    servertime_ = get_servertime()
    servertime = servertime_[0]
    nonce = servertime_[1]

    postdata['su'] = su
    postdata['sp'] = get_sp(servertime, nonce)
    postdata['servertime'] = servertime
    postdata['nonce'] = nonce

    url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'  # 抓包看到的请求网址

    req = html.post(url, data=postdata, headers=headers_)
    text = req.text

    login_url = re.findall(r'http:[^,]*=0',text)
    login_url = login_url[0]
    a = html.get(login_url)
    b = html.get('http://www.weibo.com').text
    # print(b)
    my_id = re.findall(r'(?<=CONFIG\[\'uid\'\]=\')[0-9]*(?=\';)', b)    
    my_id = my_id[0]

def get_ouid():
    global ouid
    ouid_url = input('输入目标主页的网址(建议输完加一个空格): ')
    id_page = html.get(ouid_url).text
    ouid = re.findall(r'(?<=tbinfo=\\"ouid=)[^"]*(?=\\")', id_page)  
    try:                # 在这里有时会莫名获取不到ouid, 然后再试一下就好了
        ouid = ouid[0]
    except:
        print('获取ouid失败,请再试一次')
    return ouid


def like_in_sec():
    page = html.get('http://www.weibo.com')
    page = page.text
    print(page)

    user_list = re.findall(r'(?<=mrid=)[^>]*(?=feed_list_item)', page) 

    for item in user_list:           
        # 对于每一个item, 即每一条po作分析
        string = str(item)
        judge_id = re.findall(r'(?<=tbinfo=\\\"ouid=)[0-9]*', string) # 对于普通用户和会员用户这里有细微差异, 所以就到数字就可以了
        judge_id = judge_id[0]

        if judge_id == ouid:        # 如果ouid正确
            judge_mid = re.findall(r'(?<=mid=\\\")[0-9]*(?=\\\")', string)
            judge_mid = judge_mid[0]

            # 纠正了使用rid的错误, 每条po的mid固定, 但是rid是在变的
            if judge_mid not in list:       # 此rid不在list里面, 说明是新的po, 也防止重复点赞(重复点会取消
                list.append(judge_mid)
                file.write(judge_mid + '\n')     # 更新这两个地方, 然后发包
                rid = re.findall(r'(?<=rid=)[^\\]*(?=\\\")', string)
                rid = rid[0]

                like_data['mid'] = judge_mid
                like_data['rid'] = rid
                r = html.post(like_url, data=like_data, headers=headers_)
                print(time.ctime())
                print('已点赞: 微博mid: ' + judge_mid)
                print('\n')


if __name__ == '__main__':

    login()

    filename = get_ouid() + '.txt'   # 文件以ouid.txt命名, 里面存mid列表
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

    headers_['X-Requested-With'] = 'XMLHttpRequest'
    headers_['Referer'] = 'http://www.weibo.com/u/' + my_id + '/home?leftnav=1'

    while True:
        like_in_sec()
        time.sleep(3)       
