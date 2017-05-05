import queue2
import easygui

def filterForTargets():
	queue2.mainProcess()


i=easygui.msgbox("Click to start the System Module 2", title="Verify")
if i=='OK':
	filterForTargets()
	   
 