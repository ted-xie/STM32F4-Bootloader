__author__ = 'Ted Xie'

class GeneralHelper:
    def __init__(self):
        print "=========================================================="
        print "                    STM32F4 Bootloader                    "
        print "                     (c) Ted Xie 2014                     "
        print "=========================================================="
        print ""
        print "For all commands, type \'help\' and press Enter"
        print "To return to this screen, type \'help -m\' and press Enter"
        print ""

    def setupHelp(self):
        print "   Initialization steps:"
        print "1) Connect +5V voltage source to GPIO CN4 P11"
        print "2) Ensure that CN2 P13 is not connected to anything (voltage is 0V)"
        print "3) Restart microcontroller with reset button or disconnecting/reconnecting power supply"
        print "4) Run the command \'comsetup\'"
        print "5) Choose the COM port connected to your STM32"
        print "6) Run the bootGET command"
        print "7) Use \'cd\' to find the directory of the .bin file you wish to write to the board"
        print "8) Once you are in the directory, type \'choose [filename]\', where \'filename\' is the"
        print "   name of the file you want to write, without brackets."
        print "   Alternatively, you can at any point type in \'choose [filepath]\' where \'filepath\'"
        print "   is the explicit file path of the .bin file."
        print "9) Run the \'flash\' command"
        print ""
        print "To return to this screen, type \'help -s\' and press Enter"