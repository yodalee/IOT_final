#from twisted.web.client import FileBodyProducer
#from twisted.protocols import basic
from twisted.internet import reactor
#from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from bottle import route, run, template
import pycurl
from udpwkpf import WuClass, Device
import sys
import json
import os




if __name__ == "__main__":

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
            
            #used by downstream, not implement
            #self.sendcurl('/regist/testing/10.5.6.248/33333')

		    
            f = open('deviceconf.txt','r')
            self.deviceid = f.readline()
            f.close()

	        print "test init success"
	
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

                if self.id != (int)(obj.getProperty(0)):
                    self.id = (int)(obj.getProperty(0))
                    self.obj = obj
                    print 'seld.id' + str(self.id)
                    #self.myMQTTClient.subscribe('Device/'+str(self.id)+'/L/Recv', 1, self.LCallback)
                    #self.myMQTTClient.subscribe('Device/'+str(self.id)+'/R/Recv', 1, self.RCallback)
                if pID == None:
                    #check if server sent command
                    ff=open('servercommand.txt','r')
                    servercmd = ff.readline()
                
                    if servercmd == '1':
                        print 'servercmd = 1'
                    elif servercmd == '2':
                        print 'servercmd = 2'
                    elif servercmd == '4':
                        print 'servercmd = 4'
                    elif servercmd == '0':	
                        print 'servercmd = 0'
                    ff.close()
                    print 'REST server pID=None'
                if pID == 0:
                    #pir
                    #value =  obj.getProperty(0)
                    value = val;
                    query = '/pir/'+self.deviceid+'/in/'+str(value)                
                    sendcurl(query)

                    print 'REST server pID=0'
                if pID == 1:
                    #light sensor
                    #value = obj.getProperty(1)
                    value = val
                    query = '/lightsensor/'+self.deviceid+'/in/'+str(value)                
                    sendcurl(query)
    
                    print 'REST server pID=1'
                if pID == 2:
                    #touchpad
                    #value = obj.getProperty(2)
                    value = val
                    query = '/touchpad/'+self.deviceid+'/in/'+str(value)                
                    sendcurl(query)
                    print 'REST server pID=2'
            '''
            if pID == 3:
                print pID
                mess = json.dumps({'fire': val})
                #self.myMQTTClient.publish('Device/'+str(self.id-1)+'/R/Recv', mess, 0)
            if pID == 4:
                print pID
                mess = json.dumps({'fire': val})
                #self.myMQTTClient.publish('Device/'+str(self.id+1)+'/L/Recv', mess, 0)
            '''
            except IOError:
                print 'Error'
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
