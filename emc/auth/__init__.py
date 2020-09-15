# -*- extra stuff goes here -*-
#-*- coding: UTF-8 -*-

from Products.PlonePAS.plugins.user import UserManager
from Products.PlonePAS import pas
from emc.policy.patch.pas import patch_pas
from emc.policy.patch.user import isRole


####################################
# monkey patch pas, the evil happens

pas.patch_pas = patch_pas
UserManager.isRole = isRole


#################################

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
