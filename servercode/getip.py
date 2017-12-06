# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 13:51:54 2017

@author: guojm14
"""
from IPy import IP
from scapy.all import srp,Ether,ARP,conf
import subprocess, re
import sys
import socket
fop=open('initlog.txt','w')

import os
os.system('chmod 777 initlog.txt')
def get_net_address(ifname):
    row = {}
    ipconfig_process = subprocess.Popen(["ifconfig",ifname], stdout=subprocess.PIPE)
    output = ipconfig_process.stdout.read()
 
    #获取IP
    ip_str = '([0-9]{1,3}\.){3}[0-9]{1,3}'
    ip_pattern = re.compile('(inet 地址:%s)' % ip_str)
    pattern = re.compile(ip_str)
    for ipaddr in re.finditer(ip_pattern, str(output)):
        ip = pattern.search(ipaddr.group())
        row['ip'] = ip.group()
 
    #获取子网掩码
    mask_str = '0x([0-9a-f]{8})'
    pattern = re.compile(mask_str)
    mask_pattern = re.compile(r'掩码:%s' % ip_str)
    pattern = re.compile(ip_str)
    for maskaddr in mask_pattern.finditer(str(output)):
        mask = pattern.search(maskaddr.group())
        row['mask'] = mask.group()
 
    #获取MAC
    mac_str ='([a-zA-Z0-9]{1,2}\:){5}[a-zA-Z0-9]{1,2}'
    mac_pattern = re.compile('(硬件地址 %s)' % mac_str)
    pattern = re.compile(mac_str)
    for mac_addr in re.finditer(mac_pattern, str(output)):
        mac = pattern.search(mac_addr.group())
        row['mac'] = mac.group()
    return row
def ip_init():
    ifconfig = get_net_address('wlp2s0')
    print ifconfig
    ipscan= IP(ifconfig['ip']).make_net(ifconfig['mask']).strNormal()
    print ipscan
    ip=''
    print('scaning')
    while ip=='':
        ip=getip(ipscan)
        print('.')
    fop.write(str(ip))
    address=(ip,31424)
    sock1=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock1.sendto('wojiushi '+ifconfig['ip'],address)
    sock1.close()
    sock2= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock2.bind(('0.0.0.0',31424))
    hello,_=sock2.recvfrom(1024)
    if hello=='laosiji666':
        print 'init finish'
    return ip
def getip(ipscan):
    ip=''
    try:
        ans,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ipscan,hwdst="ff:ff:ff:ff:ff:ff"),timeout=50,verbose=False)
    except Exception,e:
        print str(e)
    else:
        for snd,rcv in ans:
            #list_mac=rcv.sprintf("%ARP.hwsrc% - %ARP.psrc%")
            #print list_mac
            if rcv.hwsrc=='b8:27:eb:47:d4:d3':
                ip= rcv.psrc
                return ip
    return ip
ip_init()

