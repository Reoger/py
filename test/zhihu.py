import requests
from requests.adapters import HTTPAdapter
# import urllib
# import urllib2
import cookielib
import re
import time
import os.path
from PIL import Image

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'
headers = {'User-Agent': user_agent}

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print "12"


def get_xsrf():
    index_url = "http://www.zhihu.com"
    index_page = session.get(index_url, headers=headers)
    html = index_page.text
    pattern = r'name="_xsrf" value="(.*?)"'
    _xsrf = re.findall(pattern, html)
    return _xsrf[0]


def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r' + t + "&type=login"
    print captcha_url
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print u'captcha.jpg 所在目录:%s, 手动输入' % os.path.abspath('captcha.jpg')
    captcha = input("input captcha\n")
    return captcha


def isLogin():
    url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(url, allow_redirects=False).status_code
    print "login code: ", login_code
    if int(x=login_code) == 200:
        return True
    else:
        return False


def login(secret, account):
    if isLogin():
        print "已经登录"
        return
    if re.match(r"^1\d{10}$", account):
        print "手机号登陆\n"
        post_url = 'http://www.zhihu.com/login/phone_num'
        postdata = {
            '_xsrf': get_xsrf(),
            'password': secret,
            'remember_me': 'true',
            'phone_num': account,
        }
    else:
        print '邮箱登录\n'
        post_url = 'http://www.zhihu.com/login/email'
        postdata = {
            '_xsrf': get_xsrf(),
            'password': secret,
            'remember_me': 'true',
            'email': account,
        }
    try:
        login_page = session.post(post_url, data=postdata, headers=headers)
        login_code = login_page.text
        print login_page.status
        print login_code
        print 'what?'
    except:
        print '需要验证码'
        postdata['captcha'] = get_captcha()
        login_page = session.post(post_url, data=postdata, headers=headers)
        login_code = eval(login_page.text)  # eval 从字符串中提取字典
        u = login_code['msg']
    session.cookies.save()


def getPageCode(pageUrl):
    try:
        req = session.get(pageUrl, headers=headers)
        print req.request.headers
        return req.text
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print u"打开链接失败...", e.reason
            return None
