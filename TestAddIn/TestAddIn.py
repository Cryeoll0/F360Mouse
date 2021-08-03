#Author-
#Description-Test

import adsk.core, adsk.fusion, adsk.cam, traceback
import sys, os, pip, subprocess, time
from ctypes import c_int8
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
try:
    import hid
except:
    install("hidapi")

handlers = []

def run(context):
    global app, ui
    app = adsk.core.Application.cast(None)
    ui = adsk.core.UserInterface.cast(None)
    try: 
        app = adsk.core.Application.get()
        ui  = app.userInterface

        ui.messageBox('Start addin')

        global mouse
        mouse = hid.device()
        mouse.open(0x1b4f, 0x9206)
        mouse.set_nonblocking(True)

        camera = app.activeViewport.camera

        
        target = camera.target
        upvector = camera.upVector

        #ui.messageBox('Eye: {0}, {1}, {2} target: {3}, {4}, {5} upvector: {6}, {7}, {8}'.format(eye.x, eye.y, eye.z, target.x, target.y, target.z, upvector.x, upvector.y, upvector.z))
        
        while False: #Temporary cut of reading hid values
            report = mouse.read(64)
            if report:
                if (report[0] == 1):
                    eye = camera.eye
                    eye.x = report[1]
                    eye.y = report[2]
                    eye.z = report[3]
                    camera.eye = eye
                if (report[0] == 2):
                    rx = report[1]
                    ry = report[2]
                    rz = report[3]

        # Create the command definition.
        cmdDef = ui.commandDefinitions.addButtonDefinition('MyButtonDefIdPython', 
                                                            'Python Sample Button', 
                                                            'Sample button tooltip',
                                                            './resources')
        # Add the button the ADD-INS panel.
        addInsPanel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
        addInsPanel.controls.addCommand(cmdDef)

        # Set styles of progress dialog.
        progressDialog = ui.createProgressDialog()
        progressDialog.cancelButtonText = 'Cancel'
        progressDialog.isBackgroundTranslucent = False
        progressDialog.isCancelButtonShown = True
        
        # Show dialog
        progressDialog.show('Progress Dialog', 'Percentage: %p, Current Value: %v, Total steps: %m', 0, 50, 1)
        progressDialog.progressValue = 0
        # Draw sketches and update status.
        i = 0
        while i < 50:
            # If progress dialog is cancelled, stop drawing.
            if progressDialog.wasCancelled:
                break

            report = mouse.read(64)
            
            # Update progress value of progress dialog
            if report:
                if (report[0] == 1):
                    progressDialog.progressValue += c_int8(report[1]).value
                    i = progressDialog.progressValue
            time.sleep(0.005)
            
        # Hide the progress dialog at the end.
        progressDialog.hide()

            
                 
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        cmdDefs = ui.commandDefinitions

        ui.messageBox('Stop addin')
        mouse.close()

        buttonExample = ui.commandDefinitions.itemById('MyButtonDefIdPython')
        if buttonExample:
            # Delete the button definition.
            buttonExample.deleteMe()

            # Get panel the control is in.
            addInsPanel = ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')

            # Get and delete the button control.
            control = addInsPanel.controls.itemById('MyButtonDefIdPython')
        if control:
            control.deleteMe()


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
