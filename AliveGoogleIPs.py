# ! /usr/bin/evn python
# -*- coding: utf-8 -*- 

import Queue
import time
import sys
import threading
import urllib2
import re
import socket

class AliveGoogleIPs(object):
    def __init__(self):
        self.url = "https://github.com/justjavac/Google-IPs"
        self.ip_queue =Queue.Queue()
        self.pool = [ ]
        
    def get_googleips_in_url(self):
        html_page = urllib2.urlopen(self.url, timeout=20)
        html_context = html_page.read()
        all_ip = re.findall(r'\d+\.\d+\.\d+\.\d+', html_context)
        for ip in all_ip:
            self.ip_queue.put(ip)
        print "Get %d IPS from %s " % (self.ip_queue.qsize(),self.url)
        
    def test_available_googleips(self,ip):
        try:
            socket.setdefaulttimeout(1)
            s=socket.socket()
            start=time.time()
            s.connect((ip, 443))
            end=time.time()
            s.close()
            connect_time = end -start
            if int(connect_time*1000) < 100:
                print "%s %sms" % (ip,str(int(connect_time*1000)))
        except:
            #print "time out"
            s.close()
            
    def do_work(self):
        while True:
            ip = self.ip_queue.get()
            if ip is not None:
                self.test_available_googleips(ip)
            else:
                return
                
    
    def thread_pool_start(self):
        for i in range(300):
            work_thread =  threading.Thread(target=self.do_work)
#             daemonic = daemons
            #work_thread.setDaemon(daemonic)
            self.pool.append(work_thread)
            work_thread.start()
            
    
    def run(self):
        self.get_googleips_in_url()
        self.thread_pool_start()
        

if __name__ == "__main__":
    instance  = AliveGoogleIPs()
    instance.run()
