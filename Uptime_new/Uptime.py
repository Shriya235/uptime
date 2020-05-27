import numpy as np
import re
from itertools import chain

def uptime_check(lis,mac,len_ath,interf):
    time_list=lis
    new_list=[]
    c=0
    disconnect=0
    for x in time_list:                                                  #converting all times to minutes
        [h, m, s] = x.split(':')
        result=int(h)*60+int(m)+(int(s)/60)
        new_list.append(result)
    for a in range(len(new_list)-1):                                     #checking for adjacent times(min)
        if new_list[a]<new_list[a+1]:
            c=+1
        else:
            disconnect+=1
    print("Client= "+mac+" of interface "+interf)
    if len_ath != len(time_list):
       print('Disconnection observed due to no connection to the interface')
    else:
       print('No disconnections observed as the interface is connected')
    if disconnect!=0:
       print('No. of disconnections as uptime decreased =',disconnect)
    print('\n')   
   
def ath_mac_uptimelist(catch_start, catch_end,logfile,inter):
    results = []
    mac =[]
    m=[]
    ups=[]
    lists=[]
    upti=[]
    t=0
    every=[]
    p=re.compile(r'(?:[0-9a-fA-F]:?){12}')
    with open(logfile, 'r') as f1:
        lines = f1.readlines()
    i = 0
    while i < len(lines):
        if catch_start in lines[i]:
            t+=1
            for j in range(i + 1, len(lines)):
                if catch_end in lines[j] or j == len(lines)-1:
                    results.append(lines[i:j])
                    i = j
                    break
        else:
            i += 1
    for a in results:
        for b in a:
            if re.findall(p,b):
               m.append(b)
    for x in m:
        mac.append(re.split(r'[|\s]\s*', x))
    singlelist = list(chain.from_iterable(mac))
    mac_address=list(set(singlelist[0::29]))               #unique clients attached is found
    for p in range(len(mac_address)):                      #as the unique clients attached will vary for each interface, creating only unique no. of empty lists
        lists.append([])
        upti.append([])
    count=0
    for single_mac in mac_address:                         #taking each client
        count+=1
        for c in mac:                                      #checking for the selected client in each line having all mac address line
          if single_mac in c:             
            lists[count-1].append(c)                       #appending all the lines of 1 client in each emptylist
    for p in range(len(mac_address)):
       for abc in lists[p]:
          upti[p].append(abc[19::29])                      #accessing only uptimes of 1 client in each emptylist
    for p in range(len(mac_address)):
        uptime_check(list(chain.from_iterable(upti[p])),mac_address[p],t,inter)             #calling function to check for uptime
    
def Call_uptimelist(interface_list,fname):                 #interface_list=[ ath0,ath1,ath2 ](input) ; fname :logfile
  for interface in interface_list:
     ath_mac_uptimelist("root@RBR850:/# wlanconfig "+interface+" list sta",  "root@RBR850:/# ",fname,interface)

    


