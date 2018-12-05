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
        headers = dict(DNNAME ='CN=顾蕾,T=110101197909181550,O=JIT,C=CN',
                  CLIENTIP = '123.123.123.123'
                  )
        url = 'http://127.0.0.1:8080/Plone8/'
        rt = requests.get(url,headers=headers)      
