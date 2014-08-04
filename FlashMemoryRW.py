__author__ = 'Ted Xie'

import serial
from UserDict import UserDict

class FlashMemoryRW (UserDict):

    def __init__(self, serialPort_):
        self.ser = serial.Serial()
        self.serialPort = serialPort_

    def scanAndPrint(self):
        available = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append( (i, s.portstr))
                s.close()
            except serial.SerialException:
                pass
        print "Available serial COM ports:"

        for s in available:
            print "Number: ", s[0], " Name: ", s[1]

    def initComPort(self):
        self.ser.setBaudrate(9600)
        self.ser.setParity(serial.PARITY_NONE)
        self.ser.setPort(self.serialPort)
        self.ser.writeTimeout = 0

        if self.ser.isOpen():
            return None

        self.ser.open()
        print self.ser.name, " is now ready."

    def writeData(self, dataFile):
        print "Writing data..."
        tempFile = open(dataFile, "rb").read()

        printIndex = 0
        for c in tempFile:
            if printIndex < 16:
                print c.encode("hex"), ":",
                printIndex += 1
            else:
                print ""
                print c.encode("hex"), ":",
                printIndex = 1

        self.ser.write(tempFile)

    def receiveData(self, dataLength):
        return self.ser.read(dataLength)

    def close(self):
        self.ser.close()



if __name__ == "__main__":
    x = FlashMemoryRW(0)
    x.scanAndPrint()
    serialPortNumber = raw_input("\nPlease choose a serial port from those listed above: ")
    x = FlashMemoryRW(serialPortNumber)
    x.initComPort()
    x.writeData("FlashMemoryRW.py")

    x.close()
    exit(1)