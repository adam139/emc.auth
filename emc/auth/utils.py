# -*- coding: utf-8 -*-

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
    if len(dnsplit) == 0:
        name = ""
        idNumber = "" 
        return name,idNumber
    idNumber = dnsplit[1].rstrip()
    if idNumber.lower().index("t=") >= 0:
        idNumber = idNumber.split("=")[1]
    else:
        idNumber = ""

    for i in range(len(dnsplit)):

        if dnsplit[i].lower().index("cn=") >= 0:
            cnsplit = dnsplit[i].split("=")
            name = cnsplit[1].lstrip()
            break

        else:
            name = "dummyuser"
    return name,idNumber
                