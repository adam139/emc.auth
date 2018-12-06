#-*- coding: UTF-8 -*-
import  unittest
import os
import requests

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestRequest(unittest.TestCase):
    def test_post_dummy_jida_requests(self):
        headers = dict(DNNAME ='CN=李四,T=333010199106113321,O=JIT,C=CN',
                  CLIENTIP = '123.123.123.123'
                  )
        url = 'http://127.0.0.1:8080/Plone8/'
        rt = requests.get(url,headers=headers)      

    def test_get_dummy_refresh_requests(self):
        headers = dict(DNNAME ='CN=李四,T=333010199106113321,O=JIT,C=CN',
                  CLIENTIP = '123.123.123.123'
                  )
        url = 'http://127.0.0.1:8080/Plone8/acl_users/emc-session-plugin/refresh?session_refresh=true&amp;type=css&amp;minutes=5'
        rt = requests.get(url,headers=headers)