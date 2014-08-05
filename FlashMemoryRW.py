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
        # USART configuration:
        # 9600 baud, 8 bits, even parity, 1 stop bit
        self.ser.setBaudrate(9600)
        self.ser.setParity(serial.PARITY_EVEN)
        self.ser.setPort(portNum)
        self.ser.setStopbits(serial.STOPBITS_ONE)
        self.ser.writeTimeout = 2
        self.ser.timeout = 2

        # Buffers
        self.rxBuff = []
        self.txBuff = []

        # Command hex values
        self.GETCMD = 0x00
        self.GETVER_RPS = 0x01 # Get version and read protection status
        self.GETID = 0x02
        self.RDMEM = 0x11 # Read memory
        self.GOCMD = 0x21 # Go command
        self.WRMEM = 0x31 # Write memory
        self.ERASE = 0x43 # Erase memory
        self.WRPR = 0x63 # Write protect
        self.WRUP = 0x74 # Write unprotect
        self.RDOPR = 0x82 # Readout protect
        self.RDOUP = 0x92 # Readout unprotect

        # Constants
        self.ACK = [0x79]
        self.NACK = [0x1F]
        self.BOOTLOADER_VERSION = 0x00
        self.FLASH_SECTORS = [0x08000000, 0x08004000, 0x08008000, 0x0800C000, 0x08010000,
                              0x08020000, 0x08040000, 0x08060000, 0x08080000, 0x080A0000,
                              0x080C0000, 0x080E0000]

        if self.ser.isOpen():
            return

        self.ser.open()
        if self.ser.isOpen():
            print self.ser.name, " is now ready."
            self.ser.write([0x7F])
            self.rxBuff = []
            tempvar = self.ser.read(1)

            if len(tempvar) == 0:
                print "No ACK received for connection timing setup, exiting now."
                self.close()
                return

            self.rxBuff.append(ord(tempvar))

            if cmp(self.rxBuff, self.ACK) != 0:
                print "Error with USART connection timing."
                self.close()
                return
            print self.ser.name, " is ready for bootloading."
            return True
        else:
            return False

    def writeData(self, data):
        print "Writing data..."

        if os.path.isfile(data):
            self.ser.write(self.ACK)
            self.rxBuff = self.ser.read(1)
            print "ACK: ", self.rxBuff
            if self.rxBuff[0] != 0x79:
                print "No acknowledge signal received."
                return

            tempFile = open(data, "rb").read()
            self.ser.write(tempFile)
        else:
            for i in xrange(data):
                self.ser.write(data[i])

        print ""

    def flash(self, file):
        print "Flashing STM32..."

        if os.path.isfile(file) or os.path.isfile(os.getcwd() + "\\" + file):
            pass
        else:
            print "Not a valid file: " + file

        print "File " + file + " written successfully to STM32!"

    def bootGET(self):
        if self.ser.isOpen() == False:
            print "Must initialize serial connection first."
            return

        self.ser.write([0x00])
        self.ser.write([0xFF])

        self.rxBuff = []
        self.rxBuff.append(ord(self.ser.read(1)))
        if cmp(self.rxBuff, self.ACK) != 0 and cmp (self.rxBuff, self.NACK) != 0: # did not receive ACK or NACK
            self.ser.write(self.NACK) # send NACK
            print "Did not receive an ACK or NACK, sending NACK now."
            return
        else:
            numBytes = ord(self.ser.read(1)) + 1
            if numBytes < 11:
                print "Wrong number of bytes received. Needed 12, got ", numBytes
                return

            bytesReceived = self.ser.read(numBytes)

            self.BOOTLOADER_VERSION = ord(bytesReceived[0])
            self.GETCMD = ord(bytesReceived[1])
            self.GETVER_RPS = ord(bytesReceived[2])
            self.GETID = ord(bytesReceived[3])
            self.RDMEM = ord(bytesReceived[4])
            self.GOCMD = ord(bytesReceived[5])
            self.WRMEM = ord(bytesReceived[6])
            self.ERASE = ord(bytesReceived[7])
            self.WRPR = ord(bytesReceived[8])
            self.WRUP = ord(bytesReceived[9])
            self.RDOPR = ord(bytesReceived[10])
            self.RDOUP = ord(bytesReceived[11])

            rxByte = ord(self.ser.read(1))

            if rxByte == self.ACK[0]:
                print "Bootloader GET successful.\n"
                print "Get command: 0x%02x" % self.GETCMD
                print "Get Version and Read Protection Status: 0x%02x" % self.GETVER_RPS
                print "Get ID: 0x%02x" % self.GETID
                print "Read Memory command: 0x%02x" % self.RDMEM
                print "Go command: 0x%02x" % self.GOCMD
                print "Write Memory command: 0x%02x" % self.WRMEM
                if self.ERASE == 0x43:
                    print "Erase command: 0x%02x" % self.ERASE
                else:
                    if self.ERASE == 0x44:
                        print "Extended Erase command: 0x%02x" % self.ERASE
                    else:
                        print "Invalid erase command: 0x%02x" % self.ERASE
                print "Write Protect command: 0x%02x" % self.WRPR
                print "Write Unprotect command: 0x%02x" % self.WRUP
                print "Readout Protect command: 0x%02x" % self.RDOPR
                print "Readout Unprotect command: 0x%02x" % self.RDOUP
            else:
                print "Bootloader GET unsuccessful: did not receive final ACK"

        print "GET command done."

    def bootREAD(self, args):
        readMemAddr = 0
        if self.ser.isOpen() == False:
            print "Must initialize serial connection first."
            return

        if len(args) == 1:
            print "Must specify hex address or sector with -x or -s, respectively. \'bootread [-s|-x] [sector|addr]\'"
        elif len(args) == 2:
            print "Not enough arguments. \'bootread [-s|-x] [sector|addr]\'"
        elif len(args) == 3:
            if args[1] == "-s":
                if ord(args[2]) >= 0 and ord(args[2]) <= 11:
                    readMemAddr = self.FLASH_SECTORS[ord(args[2])]
                else:
                    print "Invalid sector number: ", args[2]
                    return
            elif args[1] == "-x":
                if ord(args[2]) >= 0 and ord(args[2]) <= 0x1FFFC00F:
                    readMemAddr = hex(args[2])
                else:
                    print "Invalid address: ", args[2]
                    return
        else:
            print "Invalid number of arguments. \'bootread [-s|-x] [sector|addr]\'"

        self.txBuff = []
        self.txBuff.append(self.RDMEM)
        self.txBuff.append(0xEE)
        self.ser.write(self.txBuff)
        self.txBuff = []
        rxin = self.ser.read(1)

        while len(rxin) == 0:
            rxin = self.ser.read(1)

        if ord(rxin) != self.ACK[0]:
            print "No ACK received for boot READ: address not yet sent."
            return


        startAddr = [0x08, 0x0E, 0x00, 0x00]
        self.ser.write(startAddr)
        chk = [0x08 ^ 0x0E ^ 0x00 ^ 0x00]
        self.ser.write(chk)

        while len(rxin) == 0:
            rxin = self.ser.read(1)

        if ord(rxin) != self.ACK[0]:
            print "No ACK received for boot READ: address already sent."
            return

        self.ser.write([255]) # 128 kB - read the whole sector 11
        self.ser.write([0]) # complement of 128 kB

        self.txBuff = self.ser.read(255)

        printIndex = 0
        for i in xrange(len(self.txBuff)):
            if printIndex < 16:
                print "%c" % ord(self.txBuff[i]),
                printIndex += 1
            else:
                print ""
                print "%c" % ord(self.txBuff[i]),
                printIndex = 1

        print "READ command done"

    def bootRDOUP(self):
        pass

    def close(self):
        self.ser.close()