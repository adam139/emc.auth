from Testing import ZopeTestCase

# BBB for Zope 2.12
try:
    from Zope2.App import zcml
except ImportError:
    from Products.Five import zcml

import emc.auth
import emc.auth.tests
from emc.auth.plugins.session import SessionPlugin

from OFS.Folder import Folder


class FakePAS(Folder):
    plugins = None

    def updateCredentials(self, request, response, userid, password):
        self.credentials = (userid, password)

    def _verifyUser(self, plugin, user_id=None, login=None):
#         assert user_id is None
        id = user_id or login
        if id == '333010199106113321':
            return dict(id=id, login=id, pluginid="emcsession")
        return None

    def _verifyUserByidNumber(self, plugin, user_id=None, login=None, idnumber=None):
        assert user_id is None
        if idnumber == '333010199106113321':
            return dict(id=idnumber, login=idnumber, pluginid="emcsession")
        return None
    

class PloneSessionTestCase(ZopeTestCase.ZopeTestCase):

    def afterSetUp(self):
        zcml.load_config('meta.zcml', emc.auth)
        zcml.load_config('configure.zcml', emc.auth)
        zcml.load_config('configure.zcml', emc.auth.tests)
        self.folder._setObject("pas", FakePAS("pas"))
        self.folder.pas._setObject("emcsession", SessionPlugin("emcsession"))


class FunctionalPloneSessionTestCase(
    ZopeTestCase.Functional,
    PloneSessionTestCase
):
    pass
