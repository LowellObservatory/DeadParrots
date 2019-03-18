#!/usr/bin/env python3
__doc__="""\
ard_tks - Arduino Tk wrapped serial interface

ard_tks.py - tkinter based UI for Arduino Serial Monitor emulation.
Uses ard_serial.py for direct communications with the Arduino
unit. The dependencies go one way only (ie ard_tks.py depends upon
ard_control.py but not vice versa).

Can be run directly from the command line:
  csh> python3 ./ars_tks.py
or
  csh> ./ars_tks.py
or from within python
  >>> import ars_tks as art
will load and start up the GUI.

For simple instructions try:
>>> print (art.__intro__)

Imports: ard_serial.py - Arduino serial communications
         sel_tks.py - UI, logging and utility building blocks

S. Levine @ Lowell Observatory (sel@enca, 2017 Dec 23)
"""
__intro__= """\
For normal operations, once the GUI is up:

1) Click "Initialize Arduino" - this will open the
   connection to the Arduino, start up the
   background thread that watches the message queues
   and sets the default parameters.

2) Click "Stop Arduino" - this will stop the threads
   and close the connection to the Arduino.

3) Click "Exit GUI" to exit the GUI.

4) Start and Stop Arduino can be used multiple times
   in a session.

5) OPEN and CLOSE will command the Arduino to OPEN
   and CLOSE the roof.

6) STOP MOTION will send a carriage return to
   interrupt a running motion.

7) HELP will display the help text from the Arduino.
"""
__author__="Stephen Levine"
__date__="2018 Jan 20"

import threading
from   time import gmtime, strftime, sleep
import tkinter    as tk

import sel_tks    as sui
import ard_serial as ars

#------------------------------------------------------------------------
class ARSGui(tk.Frame):
    def __init__(self, ardu, master=None):
        """\
        Arduino graphical user interface for Serial Monitor
        equivalent.
        Utilizes the command line driven set and wraps those
        functions with TK widgets.
        """
        super().__init__(master)

        self.artk_startup(ardu, bframe=master)

        return

    def artk_startup(self, ardu, bframe):
        """\
        Construct the GUI, and display it.
        """
        self.artk_tk_active = False
        self.artk_tailflag = False
        self.ardu = ardu
        self.pack()
        self.artk_ui_create(bframe)
        return

    def artk_exit(self):
        """\
        Stop the communications with the Arduino and
        shutdown the GUI.
        """
        self.arsg_stop()
        sui.tmGUI_exit()
        return

    def artk_ui_create(self, bframe):
        """\
        Create the GUI
        """

        # -- Button and Menu standard width
        self.std_wid  = 18
        self.mid_wid  = int(1.5 * self.std_wid)
        self.wide_wid = 3 * self.std_wid

        # -- Set up root frame
        self.artk_fr = sui.tmGUI_init(bframe)

        # -- Set up frames to hold things
        self.artk_fra  = sui.tmFrm(self.artk_fr)
        self.artk_frb  = sui.tmFrm(self.artk_fr)

        self.artk_fra.pack(side='top')
        self.artk_frb.pack(side='bottom') 

        self.artk_fra1  = sui.tmFrm(self.artk_fra)
        self.artk_fra2  = sui.tmFrm(self.artk_fra)
        self.artk_frb1  = sui.tmFrm(self.artk_frb)
        self.artk_frb2  = sui.tmFrm(self.artk_frb)

        self.artk_fra1.pack(side='top')
        self.artk_fra2.pack(side='bottom')
        self.artk_frb1.pack(side='top')
        self.artk_frb2.pack(side='bottom')

        self.artk_slog = sui.tmTxt(self.artk_fra1, sd='top', 
                                    wid=self.wide_wid, hgt=10)

        # -- search limits (end - 40lines) to (end) of Text widget
        self.artk_txt_srch_st = '{}'.format('end - 40l')
        self.artk_txt_srch_et = '{}'.format('end')

        # -- limits on how many lines to save in each of the three
        #    logging windows for scroll back - to avoid infinite growth
        #    of the memory foot print
        self.artk_txt_maxlen = 50

        # -- display gui help/welcome screen
        self.arsg_gui_help(ftime=True)

        # -- Command entry
        self.artk_cmwin, self.artk_cmwin_v = \
            sui.tmEnter(self.artk_fra2, self.arsg_send_cmd,
                         elbl='Command:', e_val=None,
                         sd='left', wd=self.wide_wid - 1)

        # -- serial port and logging file info --
        serinf, loginf = self.arsg_ser_and_log()

        self.artk_srlbl = tk.Label(self.artk_frb1, 
                                   text=serinf, width=self.mid_wid,
                                   background='gray')
        self.artk_srlbl.pack(side='left')
        self.artk_lglbl = tk.Label(self.artk_frb1, 
                                   text=loginf,
                                   width=self.mid_wid,
                                   background='gray')
        self.artk_lglbl.pack(side='right')

        # -- Action menus and buttons
        # Row 0 ---
        in_col  = 1
        in_row  = 0

        #-START Arduino ---------------------------------------
        self.artk_bt_startmot = sui.tmBtn(self.artk_frb2, blbl="Initialize Arduino",
                                          bcmd=self.arsg_startup,
                                          r=in_row, c=in_col, wd=self.std_wid,
                                          color='green')

        in_col += 1

        # Row 1 ---
        in_col  = 0
        in_row += 1

        #-OPEN ---------------------------------------
        self.artk_bt_open = sui.tmBtn(self.artk_frb2, blbl="OPEN",
                                      bcmd=self.ardu.dome_open,
                                      r=in_row, c=in_col, wd=self.std_wid)

        in_col += 1

        #-STOP MOTION ---------------------------------------
        self.artk_bt_interrupt = sui.tmBtn(self.artk_frb2, blbl="STOP MOTION",
                                           bcmd=self.ardu.dome_interrupt,
                                           r=in_row, c=in_col, wd=self.std_wid)

        in_col += 1

        #-CLOSE ---------------------------------------
        self.artk_bt_close = sui.tmBtn(self.artk_frb2, blbl="CLOSE",
                                       bcmd=self.ardu.dome_close,
                                       r=in_row, c=in_col, wd=self.std_wid)

        in_col += 1

        # Row 2 ---
        in_col  = 0
        in_row += 1

        #-HELP ---------------------------------------
        self.artk_bt_ahelp = sui.tmBtn(self.artk_frb2, blbl="Arduino Help",
                                       bcmd=self.ardu.dome_help,
                                       r=in_row, c=in_col, wd=self.std_wid)

        in_col += 2

        #-HELP ---------------------------------------
        self.artk_bt_ghelp = sui.tmBtn(self.artk_frb2, blbl="GUI Help",
                                       bcmd=self.arsg_gui_help,
                                       r=in_row, c=in_col, wd=self.std_wid)

        in_col += 1

        # Row 3 ---
        in_col  = 1
        in_row += 1

        #-STOP Arduino ---------------------------------------
        self.artk_bt_stopmot = sui.tmBtn(self.artk_frb2, blbl="Stop Arduino",
                                         bcmd=self.arsg_stop,
                                         r=in_row, c=in_col, wd=self.std_wid,
                                         color='red')

        in_col += 1

        self.artkui_quit = sui.tmBtn(self.artk_frb2, blbl="Exit GUI", 
                                     bcmd=self.artk_exit,
                                     r=in_row, c=in_col, wd=self.std_wid)

        in_col += 1

        self.artk_tk_active = True

        return

    #----------------------------------------
    # Commands to do things requested through the UI
    #----------------------------------------
    def arsg_gui_help(self,ftime=False):
        """\
        Print GUI help information.
        """
        j = 'GUI Help:\nWelcome to the 31inch Roof Control UI\n'
        j+= 'Version: {0} ({1})\n'.format(__date__, __author__)
        j+= '{}\n'.format(__intro__)
        if (ftime == True):
            self.artk_slog.insert(tk.END,j)
        else:
            self.print_lgw(j, simple=True, offset=22)

        return

    def arsg_send_cmd(self, event):
        """\
        Send a raw, unprocessed command string to the Arduino.
        """
        cmd = self.artk_cmwin_v.get()
        self.ardu.msg2ars(msg=cmd, msgname='CUSTOM', loglvl=1)
        i = ''
        self.artk_cmwin_v.set(i)
        return

    def arsg_ser_and_log(self):
        """\
        Fill in the values for the Serial Port status and the Log
        File name.
        """
        try:
            serstr = 'Serial Port: \n{}'.format(self.ardu.ars_io.port)
        except:
            serstr = 'Serial Port: \n{}'.format('Not Connected')

        logstr ='Log File: \n{}'.format(sui.lgfd.name)

        return serstr, logstr

    def arsg_startup(self):
        """\
        Start up Arduino control threads.
        """
        logtimeut = (strftime("%Y%m%d-%H:%M:%S", gmtime()))

        k = self.ardu.ars_startup()

        if (k == True):
            j = '{} ARDUINO START\n'.format(logtimeut)
        else:
            j = '{} ARDUINO START FAILED\n'.format(logtimeut)

        sui.write_log(j, dst='both')

        if (self.artk_tailflag == False):
            self.print_lgw(j)

        # -- serial port and log file info --
        serinf, loginf = self.arsg_ser_and_log()
        self.artk_srlbl.config(text=serinf)
        self.artk_lglbl.config(text=loginf)
        
        # -- start tailing the messages
        if (k == True):
            self.artk_log_spawn()

        return

    def arsg_stop(self):
        """\
        Stop Arduino control threads.
        """
        logtimeut = (strftime("%Y%m%d-%H:%M:%S", gmtime()))
        j = '{} ARDUINO STOP\n'.format(logtimeut)
        sui.write_log(j, dst='both')

        # -- stop tailing the messages
        self.artk_log_stop()

        # -- close communications with the arduino
        self.ardu.ars_stop()
        if (self.artk_tailflag == False):
            self.print_lgw(j)

        # -- serial port and log file info --
        serinf, loginf = self.arsg_ser_and_log()
        self.artk_srlbl.config(text=serinf)
        self.artk_lglbl.config(text=loginf)

        return

    def artk_log_spawn(self):
        """\
        Start up a separate thread to watch what is passing on the
        message log. sui.redir_stdout_log() causes write_log()'s
        output to stdout to go instead to the slog logging stream.
        """
        self.artk_slog_string = sui.redir_stdout_log()

        self.artk_tailflag = True
        self.artktl_thd = threading.Thread (target=self.artk_taillog)
        self.artktl_thd.name = 'ARD Log Tail Loop'
        self.artktl_thd.start()
        return

    def artk_log_stop(self):
        """\
        Set the channel watching flag to False, which will
        allow the watcher thread to exit.
        The sui.resume_stdout_log() line releases stdout back to stdout.
        """
        sui.resume_stdout_log()

        self.artk_tailflag = False
        try:
            k = self.artktl_thd.is_alive()
        except:
            k = False

        if (k == True):
            self.artktl_thd.join(timeout=1.0)
            print ('ARD logtail: {}'.format(self.artktl_thd.is_alive()))

        return

    def artk_taillog(self):
        """\
        Monitor what is passing through the logging channel.  Ideally
        this ought to be event driven, ie it blocks until when
        something new shows up, it up and then echoes that, but I
        haven't got that working yet. So, right now it has a delay
        (half the read loop time in ars_read_loop) and then compares
        the new msg to the last one.  If they differ, it
        echoes the new ones.
        """
        
        # log display frequency (Hz = cycles/sec)
        dt     = float(ars.rdloopdt/2.0)

        # oms == old log entry
        try:
            oms = ('{}\n'.format(self.artk_slog_string.getvalue()))
        except:
            oms = ''

        i = 0
        while self.artk_tailflag:
            sleep (dt)

            try:
                nms = ('{}\n'.format(self.artk_slog_string.getvalue()))
            except:
                nms = ''

            if ((nms != oms) and (nms != '')):
                self.print_lgw(nms)
                oms = nms
   
        self.artk_tailflag = False
        return

    #----------------------------------------
    # Lower level commands used by the previous ones
    #----------------------------------------
    def print_lgw (self, lgw, simple=False, offset=None):
        """\
        Print messages to a logging frame.
        Highlight UNK in red, OK, and Done in green. Searches back
        over the last 40 lines.
        """

        sui.tmPrint_lgw (lgw=lgw, slog=self.artk_slog, 
                         maxlen=self.artk_txt_maxlen,
                         srch_st=self.artk_txt_srch_st, 
                         srch_et=self.artk_txt_srch_et,
                         simple=simple, offset=offset)

        return

    #----------------------------------------
    # Widget definitions used in the UI - from sel_tks.py
    #----------------------------------------

#------------------------------------------------------------------------
# Execute the UI

if __name__ == '__main__':

# Set up the root window for the GUI
    root = tk.Tk()
    root.title('Roof Control')

# Load the arduino serial comm class
    x    = ars.ARSer(fullstart=False)

# Load the arduino gui class
    app  = ARSGui(ardu=x, master=root)

# Execute the mainloop
    app.mainloop()
