#!/usr/bin/env python3
__doc__="""\
sel_tks - Basic Tk utilities for setting up simple UIs

sel_tks.py - tkinter based functions for setting up simple UIs.

Test UI can be run directly from the command line:
  csh> python3 ./sel_tks.py
or
  csh> ./sel_tks.py
or from within python
  >>> import sel_tks as sui
will load and start up the test GUI.

For simple instructions try:
>>> print (sui.__intro__)

S. Levine @ Lowell Observatory (sel@enca, 2018 Jan 20)
"""
__intro__= """\
A small library of mid-level routines built on python and tk/tcl
as imported through tkinter.
"""
__author__="Stephen Levine"
__date__="2017 Jan 20"

import io
import sys
from time       import gmtime, strftime, sleep

try:
    import tkinter as tk
    from contextlib import redirect_stdout
except:
    pass


# Logging relate global variables
#  lgfd      == output file descriptor
#  std_red   == alternate output stream to stdout for the main log.
lgwritelg = '' # == most recent write_log() statement
lgfd      = sys.stdout
std_red   = None

# tmUI_root  == root frame for GUI
tmUI_root = None

#------------------------------------------------------------------------
# TITLE: simple_gui_create - demo routine
# Demo for setting up the skeleton of a GUI using the routines in here
#------------------------------------------------------------------------
def simple_gui_create(master):
    """\
    Create test GUI. master is the master frame within which to root this GUI.
    Typically this might be the root of the tree. So:
      root = tk.Tk()
      simple_gui_create(root)
    """

    # -- Button and Menu standard width
    std_wid  = 18
    mid_wid  = int(1.5 * std_wid)
    wide_wid = 3 * std_wid
    
    # -- Set up root frames for UI
    artk_fr = tmGUI_init(master)

    # -- Set up frames to hold things
    artk_fra  = tmFrm(artk_fr)
    artk_frb  = tmFrm(artk_fr)

    artk_fra.pack(side='top')
    artk_frb.pack(side='bottom') 

    artk_fra1  = tmFrm(artk_fra)
    artk_fra2  = tmFrm(artk_fra)
    artk_frb1  = tmFrm(artk_frb)
    artk_frb2  = tmFrm(artk_frb)

    artk_fra1.pack(side='top')
    artk_fra2.pack(side='bottom')
    artk_frb1.pack(side='top')
    artk_frb2.pack(side='bottom')

    artk_slog = tmTxt(artk_fra1, sd='top', wid=wide_wid, hgt=10)

    # -- search limits (end - 40lines) to (end) of Text widget
    artk_txt_srch_st = '{}'.format('end - 40l')
    artk_txt_srch_et = '{}'.format('end')
    
    # -- limits on how many lines to save in each of the three
    #    logging windows for scroll back - to avoid infinite growth
    #    of the memory foot print
    artk_txt_maxlen = 50

    # -- Command entry
    artk_cmwin, artk_cmwin_v = tmEnter(artk_fra2, tm_null_cmd,
                                       elbl='Command:', e_val=None,
                                       sd='left', wd=wide_wid - 1)

    # -- serial port and logging file info --
    j = 'Serial Port: \n{}'.format('Not Connected')

    artk_srlbl = tk.Label(artk_frb1, text=j, width=mid_wid,
                          background='gray')
    artk_srlbl.pack(side='left')
    artk_lglbl = tk.Label(artk_frb1, 
                          text='Log File: \n{}'.format('None'),
                          width=mid_wid, background='gray')
    artk_lglbl.pack(side='right')

    # -- Action menus and buttons
    # Row 0 ---
    in_col  = 1
    in_row  = 0

    #-START Arduino ---------------------------------------
    artk_bt_startmot = tmBtn(artk_frb2, blbl="Initialize Arduino",
                             bcmd=tm_null_cmd,
                             r=in_row, c=in_col, wd=std_wid,
                             color='green')

    in_col += 1

    # Row 1 ---
    in_col  = 0
    in_row += 1

    #-OPEN ---------------------------------------
    artk_bt_open = tmBtn(artk_frb2, blbl="OPEN",
                         bcmd=tm_null_cmd,
                         r=in_row, c=in_col, wd=std_wid)

    in_col += 1

    #-STOP MOTION ---------------------------------------
    artk_bt_interrupt = tmBtn(artk_frb2, blbl="STOP MOTION",
                              bcmd=tm_null_cmd,
                              r=in_row, c=in_col, wd=std_wid)

    in_col += 1

    #-CLOSE ---------------------------------------
    artk_bt_close = tmBtn(artk_frb2, blbl="CLOSE",
                          bcmd=tm_null_cmd,
                          r=in_row, c=in_col, wd=std_wid)

    in_col += 1

    # Row 2 ---
    in_col  = 0
    in_row += 1

    #-HELP ---------------------------------------
    artk_bt_ahelp = tmBtn(artk_frb2, blbl="Arduino Help",
                          bcmd=tm_null_cmd,
                          r=in_row, c=in_col, wd=std_wid)
    
    in_col += 2

    #-HELP ---------------------------------------
    artk_bt_ghelp = tmBtn(artk_frb2, blbl="GUI Help",
                          bcmd=tm_null_cmd,
                          r=in_row, c=in_col, wd=std_wid)
    
    in_col += 1
    
    # Row 3 ---
    in_col  = 1
    in_row += 1
    
    #-STOP Arduino ---------------------------------------
    artk_bt_stopmot = tmBtn(artk_frb2, blbl="Stop Arduino",
                            bcmd=tm_null_cmd,
                            r=in_row, c=in_col, wd=std_wid,
                            color='red')
    
    in_col += 1
    
    artkui_quit = tmBtn(artk_frb2, blbl="Exit GUI", 
                        bcmd=simple_gui_exit,
                        r=in_row, c=in_col, wd=std_wid)
    
    in_col += 1
    
    artk_tk_active = True
    
    return

def simple_gui_exit():
    """\
    Shutdown the simple GUI.
    """
    tmGUI_exit()
    return

#------------------------------------------------------------------------
# GUI init and exit
# TITLE: tmGUI_init - initialize GUI root
#------------------------------------------------------------------------
def tmGUI_init(master):
    """\
    Initialize the GUI root.
    """
    global tmUI_root

    tmUI_root = master

    # -- Set up the root frame to hold things
    tR_fr  = tmFrm(tmUI_root)
    tR_fr.pack()
    return tR_fr

# TITLE: tmGUI_init - initialize GUI root
def tmGUI_exit():
    """\
    Shutdown the GUI root
    """
    global tmUI_root

    tmUI_root.after(2000, tmUI_root.destroy)
    tmUI_root = None
    return

#------------------------------------------------------------------------
# Mid-level Widget definitions used in the UI
# TITLE: tmBtn - Setup a Button
#------------------------------------------------------------------------
def tmBtn (bbase, blbl="Button", bcmd=None, sd=None, 
           r=0, c=0, wd=25, color=None):
    """\
    Setup a Button.
    blbl == The button label
    bcmd == associated command function to execute

    Use one or the other of the following, but not both:
      sd == packing side, if using pack
      r & c == row and column if using grid
    """
    if (color == None):
        clr = 'gray'
    else:
        clr = color

    tB = tk.Button(bbase, text=blbl, command=bcmd, width=wd,
                   borderwidth=2, 
                   relief='sunken',
                   highlightbackground=clr,
                   foreground=clr)
                   # background='gray')
    if (sd != None):
        tB.pack(side=sd)
    else:
        tB.grid(row=r, column=c, padx=2, pady=1)

    return tB

#------------------------------------------------------------------------
# TITLE: tmEnter - Setup an Entry box w/ label
def tmEnter (bbase, ecmd, elbl=None, e_val=None, 
             sd=None, r=0, c=0, wd=25):
    """\
    Setup a value entry box with a label.
    ecmd is the command to be executed on <Return>.
    elbl is the leading label.

    Use one or the other of the following, but not both:
      sd == packing side, if using pack
      r & c = row and column if using grid

    wd == width, 0 means dynamic.
    """
    lwid = len(elbl) + 1
    if (lwid < wd-1):
        ewid = wd - lwid - 1
    else:
        ewid = 1

    tEL = tk.Label(bbase, text=elbl, background='gray', width=lwid)
    if (sd != None):
        tEL.pack(side=sd)
    else:
        tEL.grid(row=r, column=c, sticky='w', padx=2, pady=1)

    tEE = tk.Entry(bbase, width=ewid, borderwidth=2, relief='sunken',
                   background='gray')

    if (sd != None):
        tEE.pack(side=sd)
    else:
        tEE.grid(row=r, column=c, sticky='e', padx=2, pady=1)

    tEC = tk.StringVar()
    if (e_val != None):
        tEC.set(e_val)
    else:
        tEC.set('')

    tEE["textvariable"] = tEC
    tEE.bind('<Key-Return>', ecmd)
    return tEE, tEC

#------------------------------------------------------------------------
# TITLE: tmFrm - Setup a Frame
def tmFrm (fbase):
    """ Set up a Frame to hold other widgets."""
    tF = tk.Frame(fbase, borderwidth=2, background='gray')
    return tF

#------------------------------------------------------------------------
# TITLE: tmMenu - Setup a Menu w/in a MenuButton
def tmMenu (bbase, mcmds, mlbl=None, sd=None, r=0, c=0, 
            wd=25, dflt=0):
    """\
    Setup a Menu within a MenuButton.
    mcmds should be a dictionary with label and associated command
     passes back the selection in the StringVar associated with
     the menus tM_v, which is a flattened list, with a | separator.
     The first part is the arg to the command to be called, the 
     second part is the text label.
    mlbl == menu button label

    Use one or the other of the following, but not both:
      sd == packing side, if using pack
      r & c == row and column if using grid

    wd   == width, 0 means dynamic.
    dflt == default value (must equal a key value) to select
    """
    tMB = tk.Menubutton(bbase, text=mlbl, width=wd, background='gray')

    tM = tk.Menu(tMB)
        
    tM_v = tk.StringVar()
    tM_v.set('{} | {}'.format(-2,'UNK'))
    
    i = 0
    for key in sorted(mcmds.keys()):
        if ((dflt >= 0) and (key == dflt)):
            # print ('DFLT, KEY: ', dflt, key)
            tM_v.set('{} | {}'.format(key,mcmds[key][1]))
            i = 1

        tM.add_radiobutton(label=mcmds[key][1], command=mcmds[key][0],
                           value='{} | {}'.format(key,mcmds[key][1]),
                           variable=tM_v)

    tMB["menu"] = tM
    if (sd != None):
        tMB.pack(side=sd)
    else:
        tMB.grid(row=r, column=c, sticky='we', padx=2, pady=1)

    return tMB, tM_v

#------------------------------------------------------------------------
# TITLE: tmRdBtn - Setup a Radio Button set
def tmRdBtn (bbase, bcmds, blbl=None, sd='left', wd=25):
    """\
    Setup a Radiobutton set.
    bcmds should be a dictionary with label, associated command and
      associated variable(s).
    blbl == The button label
    sd == packing side, if using pack
    """
    tRB_v = tk.ListVar()
    i = 0
    for key in sorted(bcmds.keys()):
        if (i == 0):
            tRB_v.set(bcmds[key][1])
            i += 1

        tRB = tk.Radiobutton (bbase, text=key, 
                              command=bcmds[key][0],
                              value=bcmds[key][1], 
                              variable=tRB_v,
                              background='gray',
                              width=wd)

        tRB.pack(side=sd, anchor='w')

    return tRB, tRB_v

#------------------------------------------------------------------------
# TITLE: tmTxt - Setup a Text box
def tmTxt (bbase, wid=60, hgt=48, sd='top'):
    """\
    Setup a Text box.
    wid, hgt == width and height in characters
    sd == packing side
    """
    tT = tk.Text(bbase, width=wid, height=hgt, 
                 borderwidth=2, relief='sunken', 
                 background='gray', wrap='none')
    tT.pack(side=sd)

    # -- tags for highlighting things in Text widgets
    tT.tag_configure('blue_fg',  foreground='blue')
    tT.tag_configure('green_fg', foreground='dark green')
    tT.tag_configure('mag_fg',   foreground='magenta')
    tT.tag_configure('red_fg',   foreground='red')

    return tT


#------------------------------------------------------------------------
# Other tm support commands
#------------------------------------------------------------------------
# TITLE: tmPrint_lgw - Print messages to a logging buffer
def tmPrint_lgw (lgw, slog, maxlen=40,
                 srch_st='end - 40l', srch_et='end',
                 simple=False, offset=None):
    """\
    Print messages to a logging buffer.
    lgw    == message text
    slog   == output log buffer
    maxlen == max number of lines to retain in the log buffer def=40
    srch_st == search start point def=end-40
    srch_et == search end point def=end

    Highlight UNK in red, OK, and Done in green. Searches back
    over the last 40 lines.
    """
    
    j = lgw
    
    # get the number of the next to last line
    k = int(slog.index('end - 1l').split('.')[0])
    
    slog['state'] = tk.NORMAL
    if (k > maxlen):
        dk = '{0:f}'.format(float(k - maxlen))
        slog.delete (1.0, dk)

    slog.insert(tk.END, j)

    if (offset != None):
        kend = 'end - {}l'.format(int(offset))
    else:
        kend = tk.END

    if (simple == False):
        highlight_text(slog, 'OK',    'green_fg', start=srch_st, end=srch_et)
        highlight_text(slog, 'Done',  'green_fg', start=srch_st, end=srch_et)
        highlight_text(slog, 'START', 'green_fg', start=srch_st, end=srch_et)
        highlight_text(slog, 'Valid', 'green_fg', start=srch_st, end=srch_et)

        highlight_text(slog, 'STOP',  'red_fg',   start=srch_st, end=srch_et)
        highlight_text(slog, 'Fault', 'red_fg',   start=srch_st, end=srch_et)
        highlight_text(slog, 'FAILED','red_fg',   start=srch_st, end=srch_et)
        highlight_text(slog, 'Not valid','red_fg',   
                       start=srch_st, end=srch_et)
        highlight_text(slog, 'Not available','red_fg',
                       start=srch_st, end=srch_et)
        highlight_text(slog, 'UNK',   'mag_fg',   start=srch_st, end=srch_et)

    elif (simple == 'Help'):
        highlight_text(slog, 'HELP',  'blue_fg',  start=srch_st, end=srch_et)

    slog.see(kend)

    slog['state'] = tk.DISABLED

    return

#------------------------------------------------------------------------
def tm_null_cmd():
    """\
    Null command - place holder really for when you need a temporary
    function to bind to a widget's cmd option. Does nothing.
    """
    return

#------------------------------------------------------------------------
# Logging routines
#------------------------------------------------------------------------
# TITLE: open_log - prep log file
def open_log (lgfile=None, loglvl=0):
    """\
    Open a file for session logging.
    """
    global lgfd
    if ( lgfile != None ):
        if (lgfd != sys.stdout):
            close_log()

        lgfd = open (str(lgfile), 'a')
        logtimeut = (strftime("%Y%m%d-%H:%M:%S", gmtime()))
        write_log ('{0:s} LOGGING START\n'.format(logtimeut), dst='both')
        print ('Log Opened: ', lgfile)

    else:
        lgfd = sys.stdout

    return

#------------------------------------------------------------------------
# TITLE: close_log - end log file
def close_log (loglvl=0):
    """\
    Close log file.
    """
    global lgfd
    if ( lgfd != sys.stdout ):
        logtimeut = (strftime("%Y%m%d-%H:%M:%S", gmtime()))
        write_log ('{0:s} LOGGING END\n'.format(logtimeut), dst='both')

        lgfd.close()
        print ('Log Closed')

        lgfd = sys.stdout

    return

#------------------------------------------------------------------------
# TITLE: redir_stdout_log - redirect stdout to an io stream
def redir_stdout_log (stream=None):
    """\
    Setup an io stream for logging, and link it so that 
    write log uses that for redirecting stdout.
    If you pass in an existing io stream, it will use that, otherwise
    it will open and link to a new one.
    """
    global std_red

    if (stream == None):
        std_alternate = io.StringIO()
    else:
        std_alternate = stream

    std_red = std_alternate

    return std_alternate

# TITLE: resume_stdout_log - stop redirection to alternate stream
def resume_stdout_log ():
    """\
    Stop redirecting stdout to alternate stream.
    write log uses that for redirecting stdout.
    """
    global std_red

    std_red = None

    return

#------------------------------------------------------------------------
# TITLE: write_log - write a message to the log file and/or stdout
def write_log (message, dst=None):
    """\
    Write a message to the log file, or the stdout, or both.
    If there is no open log file, and both are requested, it
    only writes to the stdout.

    It std_red != None, then it will re-direct stdout to std_red.
    E.g. for how std_red streams are are setup:
        self.artk_slog_string = io.StringIO()
        ars.std_red = self.artk_slog_string
    will push output into self.artk_slog_string instead of stdout.
    std_red is declared at the top of this file.
    """
    global lgfd
    global lgwritelg

    lgwritelg = message

    if ((dst == None) or (dst == 'stdout') or (dst == 'both')):
        if (std_red != None):
            with redirect_stdout (std_red):
                sys.stdout.write(message)
        else:
            sys.stdout.write(message)
            
    if ((dst == 'log') or (dst == 'Log') or (dst == 'both')):
        lgfd.write(message)
        lgfd.flush()
        
    return

#------------------------------------------------------------------------
# Low level more generic routines
#------------------------------------------------------------------------
# TITLE: highlight_text - highlight strings in text display
def highlight_text(itxt, pattern, tag, start="1.0", end="end",
                      regexp=False):
    """\
    Courtesy of the internet
    https://stackoverflow.com/questions/3781670/how-to-highlight-text-in-a-tkinter-text-widget
    Modified from a method to be just a function so I could avoid modifying
    the definition of tk.Text.
    Apply the given tag to all text that matches the given pattern
    If 'regexp' is set to True, pattern will be treated as a regular
    expression according to Tcl's regular expression syntax.
    """

    start = itxt.index(start)
    end = itxt.index(end)
    # print ('start, end = ', start, end)
    itxt.mark_set("matchStart", start)
    itxt.mark_set("matchEnd", start)
    itxt.mark_set("searchLimit", end)
    
    count = tk.IntVar()

    while (True):
        index = itxt.search(pattern, "matchEnd","searchLimit",
                            count=count, regexp=regexp)
        if (index == ""): break

        j = count.get()
        # print ('j = ', j)

        if (j == 0):
            break # degenerate pattern which matches zero-length strings

        # print ('idx = ', index)
        itxt.mark_set("matchStart", index)
        itxt.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
        itxt.tag_add(tag, "matchStart", "matchEnd")

    return

#------------------------------------------------------------------------
# TITLE: isainumber - check if a string is an integer number
def isainumber(a):
    """Q&D test to see if a string is an integer number.
    Courtesy of the internet, slightly modified.
    """
    try:
        int(a)
        bool_a = True
    except:
        bool_a = False

    return bool_a

#------------------------------------------------------------------------
# TITLE: isanumber - check if a string is an floating point number
def isanumber(a):
    """Q&D test to see if a string is a floating point number.
    Courtesy of the internet, slightly modified.
    """
    try:
        float(a)
        bool_a = True
    except:
        bool_a = False

    return bool_a

#------------------------------------------------------------------------
# Execute the demo GUI

if __name__ == '__main__':

# Set up the root window for the GUI
    root = tk.Tk()
    root.title('Simple GUI')

# Start up the GUI
    simple_gui_create(root)

# execute the mainloop
    tmUI_root.mainloop()
