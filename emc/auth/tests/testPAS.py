# -*- coding: utf-8 -*-
from DateTime import DateTime
from zope.publisher.browser import TestRequest
from emc.auth.interfaces import ISessionPlugin
from emc.auth.tests.sessioncase import FunctionalPloneSessionTestCase

import six


class MockResponse(object):

    def setCookie(self, name, value, path,
                  expires=None, secure=False, http_only=False):
        self.cookie = value
        self.cookie_expires = expires
        self.cookie_http_only = http_only
        self.secure = secure


class TestSessionPlugin(FunctionalPloneSessionTestCase):

    userid = '333010199106113321'
    dn = u"CN=李四,T=333010199106113321,O=JIT,C=CN,dummychar,otherstring".encode('utf-8').decode('latin-1').encode('latin-1')
    username = u"test1".encode('utf-8').decode('latin-1').encode('latin-1')

    def testInterfaces(self):
        session = self.folder.pas.emcsession
        self.assertEqual(ISessionPlugin.providedBy(session), True)

    def makeRequest(self, cookie,dn,username):
        session = self.folder.pas.emcsession
        return TestRequest(**{session.cookie_name: cookie,"HTTP_DNNAME":dn,"username":username})

    def makeInitRequest(self, dn,username):
        session = self.folder.pas.emcsession
        return TestRequest(**{"HTTP_DNNAME":dn,"username":username})

    def makeTruecookieRequest(self,cookie, dn,username):
        session = self.folder.pas.emcsession
        cookie = session._initCookie(self.userid,user_data=cookie)

        return TestRequest(**{session.cookie_name: cookie,"HTTP_DNNAME":dn,"username":username})

    def testOneLineCookiesOnly(self):
        longid = "x" * 256
        response = MockResponse()
        session = self.folder.pas.emcsession
        session._setupSession(longid, response)
        self.assertEqual(len(response.cookie.split()), 1)

    def testCookieLifetimeNoExpiration(self):
        response = MockResponse()
        session = self.folder.pas.emcsession
        session._setupSession(self.userid, response)
        self.assertEqual(response.cookie_expires, None)

    def testSecureCookies(self):
        response = MockResponse()
        session = self.folder.pas.emcsession

        session._setupSession(self.userid, response)
        self.assertEqual(response.secure, False)

        setattr(session, 'secure', True)
        session._setupSession(self.userid, response)
        self.assertEqual(response.secure, True)

    def testCookieHTTPOnly(self):
        response = MockResponse()
        session = self.folder.pas.emcsession
        session._setupSession(self.userid, response)
        self.assertEqual(response.cookie_http_only, True)

    def testCookieLifetimeWithExpirationSet(self):
        response = MockResponse()
        session = self.folder.pas.emcsession
        session.cookie_lifetime = 100
        session._setupSession(self.userid, response)
        self.assertEqual(
            DateTime(response.cookie_expires).strftime('%Y%m%d'),
            (DateTime() + 100).strftime('%Y%m%d'),
        )

    def testExtraction(self):
        session = self.folder.pas.emcsession

        request = self.makeRequest("test string".encode("base64"),self.dn,self.username)
        creds = session.extractCredentials(request)

        self.assertEqual(creds["source"], "emc.session")
        self.assertEqual(creds["cookie"], "")

        request = self.makeRequest("test string",self.dn,self.username)
        creds = session.extractCredentials(request)
        self.assertEqual(creds, {})
        
    def testInitExtraction(self):
        session = self.folder.pas.emcsession
        request = self.makeInitRequest(self.dn,self.username)
        creds = session.extractCredentials(request)
        self.assertEqual(creds["source"], "emc.session")
        self.assertEqual(creds['init_login'], True)
#         cookie = session._initCookieNobase64(self.userid)
        self.assertEqual(creds["cookie"], "")
#         self.assertEqual(creds["cookie"], cookie)
       

    def testauthenticateCredentials(self):
        session = self.folder.pas.emcsession
        request = self.makeInitRequest(self.dn,self.username)
#         request = self.makeRequest("test string".encode("base64"),self.dn,self.username)
        creds = session.extractCredentials(request)
       
        auth = session.authenticateCredentials(creds)
        self.assertEqual(auth[0], self.userid)
        self.assertEqual(auth[1], self.userid)
        request = self.makeTruecookieRequest("test string".encode("base64"),self.dn,self.username)
        creds = session.extractCredentials(request)
        auth = session.authenticateCredentials(creds)
        
        self.assertNotEqual(auth, None)
        request = self.makeTruecookieRequest("test string",self.dn,self.username)
        creds = session.extractCredentials(request)      
        auth = session.authenticateCredentials(creds)
        self.assertNotEqual(auth, None)

    def testCredentialsUpdate(self):
        session = self.folder.pas.emcsession
        request = self.makeRequest("test string",self.dn,self.username)
        session.updateCredentials(request, request.response, "bla", "password")
        self.assertEqual(request.response.getCookie(session.cookie_name), None)

        session.updateCredentials(
            request,
            request.response,
            self.userid,
            "password"
        )
        self.assertNotEqual(
            request.response.getCookie(session.cookie_name),
            None
        )

    def testRefresh(self):
        session = self.folder.pas.emcsession
        request = self.makeRequest("test string",self.dn,self.username)
        session.updateCredentials(
            request,
            request.response,
            self.userid,
            "password"
        )
        cookie = request.response.getCookie(session.cookie_name)['value']
        request2 = self.makeRequest(cookie,self.dn,self.username)
        request2.form['type'] = 'gif'
        session.refresh(request2)
        self.assertNotEqual(
            request2.response.getCookie(session.cookie_name),
            None
        )

    def testUnicodeUserid(self):
        unicode_userid = six.text_type(self.userid)
        response = MockResponse()
        session = self.folder.pas.emcsession
        # This step would fail.
        session._setupSession(unicode_userid, response)

    def testSpecialCharUserid(self):
        unicode_userid = u"ãbcdéfghijk"
        response = MockResponse()
        session = self.folder.pas.emcsession
        # This step would fail.
        session._setupSession(unicode_userid, response)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSessionPlugin))
    return suite
