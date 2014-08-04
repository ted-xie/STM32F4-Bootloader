__author__ = 'Ted Xie'

######################################################################################################################
#
#                                               STM32F4 Bootloader
#                                               (c) 2014 Ted Xie
#
#
#                           A simple, lightweight bootloader for the STM32F4 platform
#                               with an even simpler GUI or command-line-interface.
#
#                           Implements the protocol specified in STMicroelectronics'
#                                               AN2606 manual:
#   http://www.st.com/st-web-ui/static/active/en/resource/technical/document/application_note/CD00167594.pdf
######################################################################################################################


import serial
import os
from Tkinter import *

class FlashMemoryRW (object):
    def __init__(self):
        self.ser = serial.Serial()
        self.availablePorts = []

    def scanAndPrint(self):
        available = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append( (i, s.portstr))
                s.close()
            except serial.SerialException:
                pass
        print "Found " + str(len(available)) + " available serial COM ports:"

        for s in available:
            print "\t", s[1]
            self.availablePorts.append(s[1])

    def initComPort(self, portNum):
        self.ser.setBaudrate(9600)
        self.ser.setParity(serial.PARITY_NONE)
        self.ser.setPort(portNum)
        self.ser.writeTimeout = 0
        self.ser.timeout = 2

        if self.ser.isOpen():
            return

        self.ser.open()
        if self.ser.isOpen():
            print self.ser.name, " is now ready."
            return True
        else:
            return False

    def writeData(self, data):
        print "Writing data..."

        if os.path.isfile(data):
            tempFile = open(data, "rb").read()
            self.ser.write(tempFile)
        else:
            for i in xrange(data):
                self.ser.write(data[i])

        print ""

    def receiveData(self, dataLength):
        return self.ser.read(dataLength)

    def close(self):
        self.ser.close()