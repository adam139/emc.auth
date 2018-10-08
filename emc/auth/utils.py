# -*- coding: utf-8 -*-

def transfer_codec(str):
    """
    将 ISO8859-1 编码的字节流解码后,再用utf-8编码
    """
#     if isinstance(str,basestring)
    return str.decode("iso-8859-1").encode("utf-8")
    
    
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
    
    """
    dnsplit = tStrDN.rstrip().split(",")
    for i in len(dnsplit):
        if dnsplit[i].lower().index("cn=") >= 0:
            cnsplit = dnsplit[i].split("=")
            dnName = cnsplit[1]
            if (dnName.lstrip().index(" ")>=0):
                dn = dnName.split(" ")
                name = dn[0]
                idNumber = dn[1]
            else:
                name = dnName
                idNumber = ""
        else:
            name = "dummyuser"
            idNumber = ""
    return name,idNumber
                