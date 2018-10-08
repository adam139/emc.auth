# -*- coding: utf-8 -*-
from zope.interface import Interface
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin

class ILoginIdHostExtractionPlugin(IExtractionPlugin):

    """ Common-case derivative.
    """

    def extractCredentials( request ):

        """ request -> { 'login' : login
                       , 'id_number' : identifier_number
                       , 'remote_host' : remote_host
                       , 'remote_addr' : remote_addr
                       , k1 : v1
                       ,   ...
                       , kN : vN
                       } | {}

        o If credentials are found, the returned mapping will contain at
          least 'login', 'id_number', 'remote_host' and 'remote_addr' keys,
          with the password in plaintext.

        o Return an empty mapping to indicate that the plugin found no
          appropriate credentials.
        """


class ISessionPlugin(Interface):
    """Session handling PAS plugin.
    """

    def _setupSession(userid, response):
        """
        Start a new session for a userid. The session will last until
        PAS indicates that the user has logged out.
        """
