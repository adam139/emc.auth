# -*- coding: utf-8 -*-
from AccessControl.SecurityManagement import getSecurityManager
from zope import event
import datetime
from emc.policy.events import AddlogoutEvent,NormalUserlogoutEvent
from emc.policy.events import AddloginEvent,NormalUserloginEvent
from emc.policy import get_ip,fmt,list2str,getfullname_orid

def login(pas,userid,ip):
        """ Handle a login for emc.auth.

        This method takes care of all the standard work that needs to be
        done when a user logs in:
        - sending a logged-in event
        """
        user=pas.getUserById(userid)

        if user is None:
            return

        loginEvent = NormalUserloginEvent(userid = getfullname_orid(user),
                                     datetime = datetime.datetime.now().strftime(fmt),
                                     ip = ip,
                                     type = 0,
                                     description = "",
                                     result = 1)
        if loginEvent.available():
            if loginEvent.is_normal_user():
                event.notify(loginEvent)
            else:
                loginEvent = AddloginEvent(adminid = getfullname_orid(user),
                                     userid = " ",
                                     datetime = datetime.datetime.now().strftime(fmt),
                                     ip = get_ip(),
                                     type = 0,
                                     description = "",
                                     result = 1)                
                event.notify(loginEvent)


def logout(REQUEST):
    """Publicly accessible method to log out a user
    """
    user = getSecurityManager().getUser()

    logoutEvent = NormalUserlogoutEvent(userid = getfullname_orid(user),
                                     datetime = datetime.datetime.now().strftime(fmt),
                                     ip = get_ip(),
                                     type = 0,
                                     description = "",
                                     result = 1)

    if logoutEvent.available():
        if logoutEvent.is_normal_user():
            event.notify(logoutEvent)
        else:
            logoutEvent = AddlogoutEvent(adminid = getfullname_orid(user),
                                     userid = " ",
                                     datetime = datetime.datetime.now().strftime(fmt),
                                     ip = get_ip(),
                                     type = 0,
                                     description = "",
                                     result = 1)
            event.notify(logoutEvent)            

        
def transfer_codec(str):
    """
    将 ISO8859-1 编码的字节流解码后,再用utf-8编码
    """
#     if isinstance(str,basestring)
    try:
        out = str.decode("latin-1")
    except:
        out = str
    return out
    
    
def split_idNumber(tStrDN):
    """
        String[] dnsplit = tStrDN.trim().split(",");
        for(int i=0;i<dnsplit.length;i++){
            if(dnsplit[i].toLowerCase().indexof("cn=") >= 0){
                String[] cnsplit = dnsplit[i].split("=");
                dnName = cnsplit[1];
                if(dnName.trim().indexOf(" ")>=0){
                    String[] dn = dnName.split(" ");
                    name=dn[0];
                    idNumber=dn[1];
                }else{
                    name=dnName;
                    idNumber=defaultVal;
                }
            }
        }
    example :tStrDN = "cn=test1 430203198512096013,dummychar,otherstring"
    dnname:CN=李四,T=333010199106113321,O=JIT,C=CN
    """
    
    dnsplit = tStrDN.rstrip().split(",")
    if len(dnsplit) == 0:#         name = ""
        idNumber = "" 
        return idNumber,idNumber

    dnsplit = filter(lambda x:x.lower().find("t=") >= 0,dnsplit)
    if len(dnsplit) > 0:
        idNumber = dnsplit[0].rstrip()    
        idNumber = idNumber.split("=")[1]
    else:
        idNumber = ""
    return idNumber,idNumber
                