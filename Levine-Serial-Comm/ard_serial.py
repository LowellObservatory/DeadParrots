#!/usr/bin/env python3
__doc__="""\
ard_serial.py - Simple serial interface for an Arduino.

ard_serial is a simple serial interface for an Arduino. It is meant to
fill much the same niche as the Arduino IDE Serial Monitor.

S. Levine @ Lowell Observatory (sel@ell, 2017 Dec 21)

To load and run:

1) import ard_serial as ars    # import the serial code.
2) x=ars.ARSer()               # This attaches the class defs and runs:
        x.ars_startup()        # which calls:
        ars.open_log() # start logging - opens file for today UT
        x.ars_open()   # open the serial port
        x.ars_spawn()  # spawn the listener and logger

5) Individual commands are sent as (e.g.):
 x.msg2ars(msgargs='Text', loglvl=3)

To shutdown:
7) x.ars_stop()             # Closes everything down. Calls:
      x.ars_shutdown()      # stops the listener and logger threads
      x.ars_close()         # closes the serial port
      ars.close_log()       # close out the log

8) Exit python with quit() or ^D

Installation:
 You will need a reasonably up to date python3 installation, and the
 pySerial module.
 1) Get python from www.python.org
 2) Once python is installed, use pip to get pySerial:
    pip install pySerial
 3) If you also plan to use ard_tks.py, the python/Tk based GUI that
    can be used as an overlay to ard_serial.py, then you need to make
    sure tkinter is installed too. It usually is. Check by doing an
      import tkinter as tk
    If it throws an error, exit python3 and try
      pip install tkinter

Sample installation sequence:
 yum install python3 (may need python3.i686, or python3.x86_64)
 yum install python3-pip.noarch

 yum install python3-tkinter (or .i686, or .x86_64)
 yum install pyserial.noarch (on old CentOS only finds python2 version)
or
 pip3 install pyserial
 pip3 install tkinter

Imports: sel_tks.py - UI, logging and utility building blocks

"""
__author__="Stephen Levine"
__date__="2018 Jan 27"

import glob
import os
import serial
import sys
import threading
from   time     import gmtime, strftime, sleep

from sel_tks    import isainumber, open_log, close_log, write_log

# Logging: later we can set the log file to a file, default to stdout
#  LG_DEF    == default logging level
#  lglastreq == most recent request to Arduino (timestamp, reqName, req)
#  lglastmsg == most recent message back from Arduino (timestamp, msgName, msg)
#  lgwritelg == most recent write_log() statement
#  rdloopdt  == read loop delay time - see ars_read_loop
LG_DEF    = 1
LG_MSGIN  = 0
lglastreq = ['', '', '']
lglastmsg = ['', '', '']
lgwritelg = ['']
rdloopdt  = 0.1

#------------------------------------------------------------------------
# TITLE: CLASS ARSer - Setup Arduino Comm.
class ARSer:

    def __init__(self, fullstart=True, altlog=None):
        """\
        ARSer initializations:
        If fullstart == True, then open the log, open the serial
        port and start the threads.
        Otherwise, the user will have to do those steps by hand.
        altlog is an alternate log file name to be passed to open_log().
        """
        self.arser_version = __date__
            
        # Serial I/O: io will be the serial.Serial class
        #             pending is the number of bytes waiting to be read
        self.ars_io = ''
        self.ars_pending = 0
        
        self.runflag = False
        if ( fullstart ):
            self.ars_startup(altlog=altlog)
        return

    #------------------------------------------------------------------------
    # Send messages to the Arduino
    # TITLE: msg2ars - construct host to Arduino
    def msg2ars (self, msg="0", msgname=None, loglvl=LG_DEF):
        """\
        Routine to send out an ASCII message to the Arduino
        All messages are terminated with LF (check on this)
        loglvls:
        0 - nothing
        1 - CMD request line
        2 - echo inbound message dictionary
        3 - echo outbound request dictionary
        """

        global lglastreq

        # logging time stamp
        logtimeut = (strftime("%Y%m%d-%H:%M:%S", gmtime()))
        
        # construct the actual message
        basemsg = msg
        msgout = basemsg + '\n'
    
        try:
            self.ars_io.write(bytes(msgout.encode('utf-8')))
            
        except:
            write_log ('Failed to write to Arduino - not open? Msg={}\n'\
                           .format(basemsg), dst='both')
            return
    
        # echo into the lglastreq list
        lglastreq = [logtimeut, msgname, basemsg]

        # echo to the log if desired
        if (loglvl > 0):
            j = '{0:s} (CMD {1}) {2}\n'.format(logtimeut, msgname, basemsg)
            write_log (j, dst='log')
            j = '{0}\n'.format(basemsg)
            write_log (j, dst='stdout')
            
        return
            
    #------------------------------------------------------------------------
    # Read messages from the Arduino
    # TITLE: ars2msg - read message from the Arduino
    def ars2msg (self, loglvl=LG_DEF):
        """\
        Routine to read an ASCII message from the Arduino
        All messages are terminated with LF
        
        loglvls:
        0 - nothing
        1 - echo MSGIN line
        2 - echo Number of Bytes in the read buffer
        3 - dump the message dictionary
        4 - echo the message decoding
        """

        global lglastmsg

        # The inbound buffer maxes out at 4095 bytes waiting (check on this).
        try:
            self.ars_pending = self.ars_io.in_waiting
        except:
            self.ars_pending = -1

        if (loglvl > 1):
            print ('NumBytesWaiting=', self.ars_pending)

        try:
            msgin = str(self.ars_io.readline ())
        except:
            msgin = ''
        
        if (loglvl > 3):
            print ( 'MSGIN=', msgin )

        # clean off the leading b' and trailing \r\n'
        idstart  = 2
        crlfloc  = msgin.find('\r\n')
        msg      = msgin[idstart:crlfloc-4]
    
        #    msgargs  = msgargs.replace('\r\n', '')

        # logging time stamp
        logtimeut = (strftime("%Y%m%d-%H:%M:%S", gmtime()))

        # echo into the lglastmsg list
        lglastmsg = [logtimeut, 'IN', msg]

        # echo to the log if desired
        # if loglvl < 0, presumes you want to log a SPECIFIC message, with
        #  an id == abs(loglvl) - gets written ONLY to the log
        if (loglvl > 0):
            j = '{0:s} (MSG) {1}\n'.format(logtimeut, msg)
            write_log (j, dst='log')
            j = '{0}\n'.format(msg)
            write_log (j, dst='stdout')

        return [msgin]

    #------------------------------------------------------------------------
    # quick start
    def ars_startup(self, altlog=None):
        """\
        Open the serial port and start the threads.
        Default log name will be constructed from the UT date.
        An alternative log name can be passed in as altlog='name'.
        """
        self.runflag = False

        if (altlog == None):
            logdate = (strftime("%Y%m%d", gmtime()))
            logname = logdate + '_ard.log'
        else:
            logname = '{}'.format(altlog)
            
        open_log (logname)
        write_log ('ars_control version: {}\n'.\
                   format(str(self.arser_version)),dst='both')
            
        k = self.ars_open()
        if (k == True):
            self.ars_spawn()
            
        return k
    
    #------------------------------------------------------------------------
    # quick stop
    def ars_stop(self):
        """\
        Shutdown the threads, and close the serial port
        """
        self.runflag = False
        self.ars_shutdown()
        self.ars_close()
        close_log()
        return
    
    #------------------------------------------------------------------------
    # ars_spawn - spin-off the read and log threads
    def ars_spawn (self):
        """\
        Spin-off a thread to read the the incoming data packets from
        the Arduino, and a second thread to periodically write to the log
        destination.
        """
        self.runflag = True

        self.arslg_thd = threading.Thread (target=self.ars_log_loop)
        self.arslg_thd.name = 'ARSer Log Loop'

        self.arsrd_thd = threading.Thread (target=self.ars_read_loop)
        self.arsrd_thd.name = 'ARSer Read Loop'

        self.arslg_thd.start()
        self.arsrd_thd.start()
        write_log ('Threads started\n', dst='both')
        return

    #------------------------------------------------------------------------
    # ars_read_loop - read the Arduino serial port
    def ars_read_loop (self):
        """\
        ARSer serial port read loop.
        The Arduino may broadcast any time. We need to keep a
        read loop running to keep up. The read buffer fills at 4095 bytes.
        Under normal circumstances, the read thread should be able to
        keep up easily.
        """
        write_log ('Read starting up\n', dst='both')
        i = 1
        while self.runflag:
            self.ars2msg (loglvl=LG_DEF)
            if ( self.ars_pending > 2048 ):
                print ('Pending Buffer =', self.ars_pending)
            elif ( self.ars_pending < 0 ):
                print ('Trouble with connection to device\n')
                sleep (rdloopdt)
            
        self.runflag = False
        write_log ('Read shutting down\n', dst='both')
        return

    #------------------------------------------------------------------------
    # ars_log_loop - handle logging
    def ars_log_loop (self):
        """\
        ARSer Logging Loop
        """
        write_log ('Log starting up\n', dst='both')
        i = 0
        while self.runflag:
            sleep (1)
            if ( i % 60 == 0 ):
                self.show_status(length=2, dst='log')
                i = 0
            i+=1
        self.runflag = False
        write_log ('Log shutting down\n', dst='both')
        return

    #------------------------------------------------------------------------
    # Thread shutdown ----------------------------------------
    def ars_shutdown (self):
        """\
        Thread shutdown in prep for overall shutdown.
        """
        self.runflag = False
        try:
            k = self.arsrd_thd.is_alive()
        except:
            k = False

        if (k == True):
            self.arsrd_thd.join(timeout=1.0)

        try:
            k = self.arslg_thd.is_alive()
        except:
            k = False

        if (k == True):
            self.arslg_thd.join(timeout=1.0)

        write_log ('Threads stopped\n', dst='both')
        return

    #------------------------------------------------------------------------
    def ars_open (self, port=None):
        """\
        Establish connection to Arduino receiver over a serial port which
        passes over USB.
        Check system platform to guess logical names for serial ports.
        Added a bit to try to determine the appropriate port. It looks
        at the ports, and checks for 'arduino' as the leading word in
        the port description. If so, the last match will be the selected
        port. If that fails, it falls back to a hard-coded guess based
        on the OS.
        """

        # expand port testing later - need appropriate names etc.
        if (port == None):

            # Try figuring out the usb port by querying available ports
            #  uses class serial.tools.list_ports_common.ListPortInfo

            import serial.tools.list_ports as stl
            j = stl.comports()
            print (j)
            for i in range(len(j)):
                kdev = j[i].device
                kdesc = '{}'.format(j[i].usb_description()).lower().split(' ')
                write_log('PORTS: {} - {}\n'.format(kdev, kdesc), dst='both')
                if (kdesc[0] == 'arduino'):
                    port = kdev

            # Try fall backs if port == None
            if (port == None):
                if (sys.platform.startswith('linux')):
                    port = '/dev/ttyUSB0'

                elif (sys.platform.startswith('darwin')):
                    port = '/dev/cu.usbmodem1421'

                elif (sys.platform.startswith('win32')):
                    port = 'COM1'

                else:
                    port = '/dev/ttyUSB0'


        # Hopefully we have a decent port ...
        write_log('Setting USB port to {}\n'.format(port), dst='both')

        k_port = os.path.exists(port)
        if (k_port != True):
            j = 'ARSer port {} is not accessible, aborting\n'.format(port)
            write_log(j, dst='both')
            return False

        baud     = 9600
        dbits    = serial.EIGHTBITS
        parity   = serial.PARITY_NONE
        stopbits = serial.STOPBITS_ONE

        try:
            k_io = self.ars_io.is_open
                
        except:
            k_io = False

        if (k_io == True):
            write_log('Arduino is already OPEN', dst='both')

        else:
            self.ars_io = serial.Serial(port=port, baudrate=baud, 
                                        bytesize=dbits, parity=parity, 
                                        stopbits=stopbits)

        if (self.ars_io.is_open == True):
            j = 'Arduino is OPEN: {}\n'.format(self.ars_io.is_open)
        else:
            j = 'Unable to open Arduino\n'

        write_log (j, dst='both')

        return self.ars_io.is_open

    #------------------------------------------------------------------------
    def ars_close (self):
        """\
        Close connection to Arduino over a serial port.
        """
        try:
            k_io = self.ars_io.is_open
        except:
            k_io = False

        if (k_io == True):
            self.ars_io.close()
            j = 'Arduino is OPEN: {}\n'.format(self.ars_io.is_open)
        else:
            j = 'Arduino is OPEN: {}\n'.format('Was not open')

        write_log (j, dst='both')
        return

    #------------------------------------------------------------------------
    def show_status (self, length=0, dst=None, loglvl=0):
        """\
        Human readable system status display.
        length = 0 - means the most important items
        1  ... 3 - get progressively more detailed
        """

        logtimeut = (strftime("%Y%m%d-%H:%M:%S", gmtime()))
        statmsg = '{0:s} SYSTEM STATUS MESSAGE\n'.format(logtimeut)
        statmsg += '{}'.format(self.ars_io)
        statmsg += '\n'

        write_log (statmsg, dst)
        return

    #----------------------------------------
    # functional level operations

    #--------------------
    def dome_open(self, ptime=None):
        """\
        Send command to open the dome/roof.
        Optional argument is the integer number of seconds
        for the Arduino to hold the line high.
        """
        k = False
        if (ptime != None):
            k = isainumber(ptime)

        j = 'OPEN'
        if (k == True):
            j += ',{0}'.format(ptime)

        self.msg2ars(msg=j, msgname='OPEN')
        return

    def dome_close(self, ptime=None):
        """\
        Send command to close the dome/roof.
        Optional argument is the integer number of seconds
        for the Arduino to hold the line high.
        """
        k = False
        if (ptime != None):
            k = isainumber(ptime)

        j = 'CLOSE'
        if (k == True):
            j += ',{0}'.format(ptime)

        self.msg2ars(msg=j, msgname='CLOSE')
        return

    def dome_interrupt(self):
        """\
        Send a character to interrupt and stop any motion that
        is currently being executed.
        """
        j = '\n'
        self.msg2ars(msg=j, msgname='INTERRUPT')
        return
        
    def dome_help(self):
        """\
        Request the help page from the Arduino.
        """
        self.msg2ars(msg='H', msgname='HELP')
        return
