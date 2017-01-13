from twisted.internet import reactor
from udpwkpf import WuClass, Device
import sys
import time

# sensor
PIR_IN = 0
TOUCH_IN = 1
LIGHT_IN = 2

# output
LIGHT_OUT = 3

# upload/download
UPLOADID = 4
UPLOADVALUE = 5
DOWNLOADID = 6
DOWNLOADVALUE = 7

class Collector(WuClass):
    def __init__(self):
        WuClass.__init__(self)
        self.loadClass('Collector')
        self.state = 0
        self.canTouch = 0
        self.lastdetect = int(time.now())
        self.close_time = 10
        self.ligthlevel = 100

        print "Collector init success"

    def upload(self, obj, uploadid, uploadvalue):
        print("upload data, id: %d, value: %d" % uploadid, uploadvalue)
        self.setProperty(UPLOADID, uploadid)
        self.setProperty(UPLOADVALUE, uploadvalue)

    def update(self,obj,pID,val):
        if pID is None:
            # const update
            t = int(time.now())
            if t - self.lastdetect > self.close_time :
                self.state = 0
                self.setProperty(LIGHT_OUT, self.state)
        else:
            if pID == PIR_IN:
                pir_in = obj.getProperty(PIR_IN)
                self.lastdetect = int(time.now())

            if pID == LIGHT_IN:
                self.lightlevel = obj.getProperty(LIGHT_IN)

            if pID == TOUCH_IN:
                # open light based on current light level
                pir_in = obj.getProperty(TOUCH_IN)

                if pir_in and canTouch:
                    self.canTouch = False
                    self.lastdetect = int(time.now())
                    if self.state == 0:
                        if self.lightlevel < 75:
                            self.state = 3
                        elif self.lightlevel < 150:
                            self.state = 2
                        else:
                            self.state = 1
                    else:
                        self.state == (self.state + 1) % 4
                else:
                    canTouch = True

                self.setProperty(LIGHT_OUT, self.state)

            if pID == DOWNLOADVALUE:
                # download logic
                dlid = obj.getProperty(DOWNLOADID)
                dlvl = obj.getProperty(DOWNLOADVALUE)

                if dlid == 1:
                    self.close_time = dlvl
                elif dlid == 2:
                    self.state = 0
                    self.setProperty(LIGHT_OUT, self.state)

if __name__ == "__main__":
    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):
            cls = Collector()
            self.addClass(cls, self.FLAG_VIRTUAL)
            self.obj_collector = self.addObject(cls.ID)

    if len(sys.argv) <= 2:
        print 'python %s <gip> <dip>:<port>' % sys.argv[0]
        print '      <gip>: IP addrees of gateway'
        print '      <dip>: IP address of Python device'
        print '      <port>: An unique port number'
        print ' ex. python %s 192.168.4.7 127.0.0.1:3000' % sys.argv[0]
        sys.exit(-1)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()

