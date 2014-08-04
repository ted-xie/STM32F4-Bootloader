__author__ = 'Ted Xie'

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
        self.pwd = "C:/"
        os.chdir(self.pwd)

        self.availableCommands = []
        self.availableCommands.append("choose")
        self.availableCommands.append("cd")
        self.availableCommands.append("help")
        self.availableCommands.append("history")
        self.availableCommands.append("ls")
        self.availableCommands.append("quit")
        self.flag()

    def log(self, cmd):
        if self.numCommandsLogged < 5:
            self.numCommandsLogged += 1
            self.last5Commands.append(cmd)
        else:
            self.last5Commands.pop(0)
            self.last5Commands.append(cmd)

    def flag(self):
        print self.pwd, ">",
        cmd = raw_input()
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
        if lineIn == "help":
            self.helpHandler(args)
        if lineIn == "history":
            self.historyHandler(args)
        if lineIn == "ls":
            self.lsHandler(args)
        if lineIn == "quit":
            self.quitHandler(args)

    def chooseHandler(self, args):
        return

    def cdHandler(self, args):
        if len(args) == 1:
            print self.pwd
        else:
            if args[1] in os.listdir(self.pwd):
                self.pwd += args[1]
                self.pwd += "/"
                os.chdir(self.pwd)
                self.flag()
                return True
            else:
                if args[1] == ".." or args[1] == "../" or args[1] == "..\\":
                    self.pwd = self.pwd[:-2]
                    tempArr = self.pwd.split('/')
                    self.pwd = ""

                    for i in range(len(tempArr) - 1):
                        self.pwd += tempArr[i]
                        self.pwd += "/"
                    os.chdir(self.pwd)
                    self.flag()
                    return True
                else:
                    print "No such file or directory: ", args[1]
                    self.flag()
                    return False
        self.flag()

    def helpHandler(self, args):
        print "Help screen goes here"
        self.flag()

    def historyHandler(self, args):
        if (len(args) == 1) or (args[1] == "-l"):
            for cmd in self.last5Commands:
                print cmd
        else:
            if args[1] == "-r":
                if args[2] in self.last5Commands:
                    self.last5Commands.remove(args[2])
                    self.numCommandsLogged -= 1
            if args[1] == "-c":
                for s in self.last5Commands:
                    self.last5Commands.remove(s)
                    self.numCommandsLogged = 0

        self.flag()

    def lsHandler(self, args):
        direcListing = os.listdir(self.pwd)
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
            self.flag()
        self.flag()

    def quitHandler(self, args):
        return

    def removeCommandFromHistory(self, cmd):
        if self.last5Commands.count(cmd) == 0:
            print "No such command in command history"
            return False
        else:
            self.last5Commands.remove(cmd)
            self.numCommandsLogged -= 1

class FlashMemoryRW (object):
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
    cmd = CommandHandler()

    exit(1)