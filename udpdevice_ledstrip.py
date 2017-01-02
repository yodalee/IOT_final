from twisted.internet import reactor
from udpwkpf import WuClass, Device
import sys
from udpwkpf_io_interface import *
import pyupm_lpd8806
import atexit
import time

# config led
nLED = 4
ledstrip = pyupm_lpd8806.LPD8806(nLED, 7)
ledOff = [0, 0, 0]
ledR = [5, 0, 0]
ledG = [0, 5, 0]
ledB = [0, 0, 5]
ledY = [5, 5, 0]
ledW = [5, 5, 5]

def setLEDStrip(l1, l2, l3, l4):
    ledstrip.show()
    ledstrip.setPixelColor(0, *l1)
    ledstrip.setPixelColor(1, *l2)
    ledstrip.setPixelColor(2, *l3)
    ledstrip.setPixelColor(3, *l4)
    ledstrip.show()

def closeLEDStrip():
    setLEDStrip(ledOff, ledOff, ledOff, ledOff)

atexit.register(closeLEDStrip)

class LED_Pattern(WuClass):
    def __init__(self):
        WuClass.__init__(self)
        self.loadClass('LED_Pattern')
        self.state = 0
        print ("LED Pattern Init Success")

    def update(self,obj,pID=None,val=None):
        try:
            if pID == None:
                if self.state == 0:
                    closeLEDStrip()
                elif self.state == 1:
                    setLEDStrip(ledOff, ledW, ledOff, ledOff)
                elif self.state == 2:
                    setLEDStrip(ledOff, ledW, ledOff, ledW)
                elif self.state == 3:
                    setLEDStrip(ledW, ledW, ledW, ledW)
                # refresh
                print("LED Pattern Refresh %d" % (self.state))

            elif pID == 0:
                # value update
                self.state = val

                print("LED_Pattern update state: %d" %(self.state))
        except IOError:
            print("LED_Pattern Error")


if __name__ == "__main__":
    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):
            m1 = LED_Pattern()
            self.addClass(m1,0)
            self.obj_counter = self.addObject(m1.ID)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()
    device_cleanup()
