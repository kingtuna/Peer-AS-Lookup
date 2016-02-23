#!/usr/bin/env python

def peer_as_cymru(IP,TIME=None,ISOT=None):
    """
    Timestamp Format: 2015-12-25 13:23:01 GMT
    Headers: PEER_AS | IP | BGP Prefix | CC | Registry | Allocated | Info | AS Name
    res = a dictionary of the headers names. spaces are converted to underscores
    """
    from datetime import datetime
    import socket
    TCP_IP = 'v4-peer.whois.cymru.com'
    TCP_PORT = 43
    BUFFER_SIZE = 1024
    BUILD = " -v " + str(IP)
    if ISOT is not None:
        NT = ISOT.strip('Z').split('T')
        TIME = NT[0] + ' ' + NT[1].split('.')[0] + ' GMT'
    if TIME is not None:
        BUILD = str(BUILD) + str(' '+ TIME+"\r\n")
    else:
        TIME = str(datetime.utcnow()).split('.')[0] + ' GMT'
        BUILD = str(BUILD) + str(' '+ TIME+"\r\n")
    MESSAGE = BUILD
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE)
    s.close()
    
    test = data.split('\n')
    answers = len(test)-1
    i = 1
    res = []
    while i < answers:
        asn = data.split('\n')[i].split('|')[0].strip()
        oip = data.split('\n')[i].split('|')[1].strip()
        ipb = data.split('\n')[i].split('|')[2].strip()
        cun = data.split('\n')[i].split('|')[3].strip()
        reg = data.split('\n')[i].split('|')[4].strip()
        alc = data.split('\n')[i].split('|')[5].strip()
        inf = data.split('\n')[i].split('|')[6].strip()
        lan = data.split('\n')[i].split('|')[7].strip()
        res.append({'PEER_AS' : asn,
               'IP' : oip,
               'BGP_Prefix' : ipb,
               'CC' : cun,
               'Registry' : reg,
               'Allocated' : alc, 
               'Info' : inf,
               'AS_Name': lan})
        i+=1
    return(res)

#Eg. '4.2.2.2 2004-12-10 11:33:21 GMT' 
print peer_as_cymru('4.2.2.2',TIME='2004-12-10 11:33:21 GMT')
print peer_as_cymru('4.2.2.2',ISOT='2004-12-10T11:33:21.000Z')
lister = peer_as_cymru('4.2.2.2')
for li in lister:
    print li
