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
ledR = [10, 0, 0]
ledG = [0, 10, 0]
ledB = [0, 0, 10]
ledY = [10, 10, 0]

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
        self.substate = 0
        print ("LED Pattern Init Success")

    def update(self,obj,pID=None,val=None):
        try:
            if pID == None:
                if self.state == 0:
                    closeLEDStrip()
                elif self.state == 1:
                    self.substate = (self.substate + 1) % 2
                    if self.substate == 0:
                        setLEDStrip(ledR, ledR, ledR, ledR)
                    elif self.substate == 1:
                        setLEDStrip(ledOff, ledOff, ledOff, ledOff)
                elif self.state == 2 or self.state == 3:
                    if self.state == 2:
                        self.substate = (self.substate + 1) % 4
                    else:
                        self.substate = (self.substate + 3) % 4

                    if self.substate == 0:
                        setLEDStrip(ledY, ledOff, ledOff, ledOff)
                    elif self.substate == 1:
                        setLEDStrip(ledOff, ledY, ledOff, ledOff)
                    elif self.substate == 2:
                        setLEDStrip(ledOff, ledOff, ledY, ledOff)
                    elif self.substate == 3:
                        setLEDStrip(ledOff, ledOff, ledOff, ledY)
                # refresh
                print("LED Pattern Refresh %d" % (self.state))
            elif pID == 0:
                # value update
                self.state = val
                if self.state == 0:
                    obj.setProperty(1, 1000000)
                elif self.state == 1:
                    obj.setProperty(1, 500)
                else: 
                    obj.setProperty(1, 200)

                print("LED_Pattern update state: %d" %(self.state))
        except IOError:
            print("LED_Pattern Error")
            

if __name__ == "__main__":
    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):
           # m1 = Counter()
           # self.addClass(m1,0)
           # self.obj_counter = self.addObject(m1.ID)

            m2 = LED_Pattern()
            self.addClass(m2,0)
            self.obj_counter = self.addObject(m2.ID)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()
    device_cleanup()
