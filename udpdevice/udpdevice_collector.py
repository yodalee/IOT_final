from twisted.internet import reactor
from udpwkpf import WuClass, Device
import sys

class Collector(WuClass):
    def __init__(self):
        WuClass.__init__(self)
        self.loadClass('Collector')
        self.state = 0
        print "Collector init success"

    def update(self,obj,pID,val):
        if pID == 0 or pID == 1:
            print "Collector update: ",
            pir_in = obj.getProperty(0)
            touch_in = obj.getProperty(1)

            if pir_in == True:
                print "pir detect"
                self.state = (self.state + 1) % 4
            elif touch_in == True:
                print "touch detect"
                self.state = (self.state - 1) % 4

            obj.setProperty(2, self.state)

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

