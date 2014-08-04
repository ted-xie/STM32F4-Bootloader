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

class BootLoaderGUI (object):
    def __init__(self):
        self.commandHandler = CommandHandler()

class CommandHandler (object):
    def __init__(self):
        self.last5Commands = []
        self.numCommandsLogged = 0
        self.selectedFilePath = ""
        self.flashReadWriter = FlashMemoryRW()
        self.pwd = os.getcwd()

        self.availableCommands = []
        self.availableCommands.append("choose")
        self.availableCommands.append("cd")
        self.availableCommands.append("comread")
        self.availableCommands.append("comsetup")
        self.availableCommands.append("comterminate")
        self.availableCommands.append("comwrite")
        self.availableCommands.append("flash")
        self.availableCommands.append("help")
        self.availableCommands.append("history")
        self.availableCommands.append("ls")
        self.availableCommands.append("quit")
        self.availableCommands.append("reset")
        self.flag()

    def log(self, cmd):
        if self.numCommandsLogged < 5:
            self.numCommandsLogged += 1
            self.last5Commands.append(cmd)
        else:
            self.last5Commands.pop(0)
            self.last5Commands.append(cmd)

    def flag(self):
        while True:
            print self.pwd + ">",
            cmd = raw_input()
            self.log (cmd)
            self.parse(cmd)

    def parse(self, lineIn):
        splitCmds = lineIn.split()
        if self.availableCommands.count(splitCmds[0]) == 0:
            print "ERROR: ", splitCmds[0], " is not a valid command."

        else:
            self.handle(splitCmds[0], splitCmds)

    def handle(self, lineIn, args):
        if lineIn == "choose":
            self.chooseHandler(args)
        if lineIn == "cd":
            self.cdHandler(args)
        if lineIn == "comterminate":
            self.flashReadWriter.close()
        if lineIn == "comread":
            self.comRead()
        if lineIn == "comsetup":
            self.comSetup()
        if lineIn == "comwrite":
            self.comWrite()
        if lineIn == "flash":
            self.flash()
        if lineIn == "help":
            self.helpHandler(args)
        if lineIn == "history":
            self.historyHandler(args)
        if lineIn == "ls":
            self.lsHandler(args)
        if lineIn == "quit":
            self.quitHandler(args)
        if lineIn == "reset":
            self.__init__()

    def chooseHandler(self, args):
        fullPath = self.pwd + "\\" + args[1]
        if os.path.isfile(fullPath):
            self.selectedFilePath = fullPath
            print "File " + fullPath + " chosen."
        else:
            print "Not a valid file: " + fullPath

    def cdHandler(self, args):
        if len(args) == 1:
            print self.pwd
            return True
        else:
            if args[1] in os.listdir(self.pwd):
                self.pwd += args[1]
                self.pwd += "\\"
                os.chdir(self.pwd)

                return True
            if os.path.isdir(args[1]):
                if args[1] == ".." or args[1] == "../" or args[1] == "..\\":
                    os.chdir(args[1])
                    self.pwd = os.getcwd()
                    return True


                strList = list(args[1])
                for i in xrange(len(args[1])):
                    if args[1][i] == '/':
                        strList[i] = '\\'

                newPath = "".join(strList)
                self.pwd = newPath
                os.chdir(self.pwd)

                return True

            else:
                print "No such file or directory: ", args[1]

                return False

    def comRead(self):
        return

    def comSetup(self):
        self.flashReadWriter.scanAndPrint()
        setupPort = raw_input("Choose a serial port: ")
        self.flashReadWriter.initComPort(setupPort)

    def comWrite(self):
        return

    def flash(self):
        return

    def helpHandler(self, args):
        print "Help screen goes here"


    def historyHandler(self, args):
        if (len(args) == 1) or (args[1] == "-l"):
            for cmd in self.last5Commands:
                print "\t" + cmd
        else:
            if args[1] == "-r":
                if len(args) >= 3:
                    if args[2] in self.last5Commands:
                        self.last5Commands.remove(args[2])
                        self.numCommandsLogged -= 1
            if args[1] == "-c":
                self.last5Commands = []
                self.numCommandsLogged = 0



    def lsHandler(self, args):
        direcListing = os.listdir(self.pwd)

        for i in range(len(direcListing)):
            if os.path.isdir(self.pwd + "\\" + direcListing[i]) == True:
                direcListing[i] = color.BLUE + direcListing[i]
                direcListing[i] += color.END

        if len(args) == 1:
            printIndex = 0
            direcListing.insert(0, "")

            for s in direcListing:
                if printIndex < 8:
                    print s,
                    printIndex += 1
                else:
                    print "\t"
                    print s,
                    printIndex = 1
            print ""
        else:
            print "\t",
            print "\n\t".join(direcListing)



    def quitHandler(self, args):
        print "Bye"
        exit(1)

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class FlashMemoryRW (object):
    def __init__(self):
        self.ser = serial.Serial()

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

    def initComPort(self, portNum):
        self.ser.setBaudrate(9600)
        self.ser.setParity(serial.PARITY_NONE)
        self.ser.setPort(portNum)
        self.ser.writeTimeout = 0
        self.ser.timeout = 2

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
    CommandHandler()

    exit(1)