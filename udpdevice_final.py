import sys
from udpwkpf import WuClass, Device
from udpwkpf_io_interface import *
from twisted.internet import reactor

import udpdevice_touch_sensor
import udpdevice_pir_sensor
import udpdevice_ledstrip
import udpdevice_collector

class MyDevice(Device):
    def __init__(self,addr,localaddr):
        Device.__init__(self,addr,localaddr)

    def init(self):
        m1 = udpdevice_touch_sensor.TouchSensor()
        self.addClass(m1, 1)
        self.obj_touch_sensor = self.addObject(m1.ID)

        m2 = udpdevice_pir_sensor.PIRSensor()
        self.addClass(m2, 1)
        self.obj_pir_sensor = self.addObject(m2.ID)

        m3 = udpdevice_ledstrip.Pattern()
        self.addClass(m3, 1)
        self.obj_ledstrip = self.addObject(m3.ID)

        m4 = udpdevice_collector.Collector()
        self.addClass(m4, self.FLAG_VIRTUAL)
        self.obj_collector = self.addObject(m4.ID)

        print("Final module init success")

if len(sys.argv) <= 2:
        print 'python udpwkpf.py <ip> <ip:port>'
        print '      <ip>: IP of the interface'
        print '      <port>: The unique port number in the interface'
        print ' ex. python udpwkpf.py 127.0.0.1 3000'
        sys.exit(-1)

d = MyDevice(sys.argv[1],sys.argv[2])
reactor.run()

