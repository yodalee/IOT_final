from twisted.internet import reactor
from bottle import route, run, template
import pycurl
from udpwkpf import WuClass, Device
import sys
import json
import os

SERVERADR = 0
DEVICEID = 1
UPLOADID = 2
UPLOADVALUE = 3
DOWNLOADID = 4
DOWNLOADVALUE = 5
<property name="serveradr" access="readwrite" datatype="string" default="" />
<property name="deviceid" access="readwrite" datatype="short" default="0" />
<property name="uploadtype" access="writeonly" datatype="short" default="0"/>
<property name="uploadvalue" access="writeonly" datatype="short" default="0"/>
<property name="downloadtype" access="readonly" datatype="short" default="0"/>
<property name="downloadvalue" access="readonly" datatype="short" default="0"/>
<property name="refresh_rate" access="readwrite" datatype="refresh_rate" default="100"  />



class GetPage:
    def __init__ (self, url):
        self.contents = ''
        self.url = url

    def read_page (self, buf):
        self.contents = self.contents + buf

    def show_page (self):
        print self.contents

class REST_Daemon(WuClass):
    def __init__(self):
        WuClass.__init__(self)
        self.loadClass('REST_Daemon')

        #init client and rest server for getting response
        self.serverIP = '10.5.6.248:23456'

        print "Rest Daemon init success"

    def sendcurl(query):
        #send query to rest server
        #query need to start with /
        target = GetPage('http://'+self.serverIP+query)
        testcurl = pycurl.Curl()
        testcurl.setopt(testcurl.URL, target.url)
        testcurl.setopt(testcurl.WRITEFUNCTION, target.read_page)
        testcurl.perform()
        testcurl.close()

    def update(self,obj,pID=None,val=None):
        try:
            if pID == None:
                #check if server sent command
                ff=open('servercommand.txt','r')
                line = ff.readline()
                if line != "":
                    servercmd = map(int, line.split(","))
                    id = servercmd[0]
                    vl = servercmd[1]
                    obj.setProperty(DOWNLOADID, id)
                    obj.setProperty(DOWNLOADVALUE, vl)
                    print("Get server cmd: %d value %d" % (id, vl))

                # clear command content
                open("servercommand.txt", "w").close()
            else:
                if pID == SERVERADT:
                    self.serverIF = obj.getProperty(SERVERADR)
                elif pID == DEVICEID:
                    self.deviceID = int(obj.getProperty(DEVICEID)
                elif pID == UPLOADVALUE:
                    print 'REST server pID=2'
                    ulid = obj.getProperty(UPLOADID)
                    ullv = obj.getProperty(UPLOADVALUE)
                    query = "/%s/%d/%d" %(self.
                    sendcurl(query)

        except IOError:
            print 'Error'

if __name__ == "__main__":
    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):
            self.m = REST_Daemon()
            self.addClass(self.m,0)
            self.obj_philip = self.addObject(self.m.ID)

    if len(sys.argv) <= 2:
        print 'python %s <gip> <dip>:<port>' % sys.argv[0]
        print '      <gip>: IP addrees of gateway'
        print '      <dip>: IP address of Python device'
        print '      <port>: An unique port number'
        print ' ex. python %s 192.168.4.7 127.0.0.1:3000' % sys.argv[0]
        sys.exit(-1)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()
