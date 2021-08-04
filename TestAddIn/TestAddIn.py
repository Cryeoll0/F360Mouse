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

        cam = app.activeViewport.camera
        cam.isSmoothTransition = False

        while True: #Temporary cut of reading hid values
            report = mouse.read(64)
            if report:
                if (report[0] == 1):
                    eye = cam.eye
                    eye.x += c_int8(report[1]).value
                    eye.y += c_int8(report[2]).value
                    eye.z += c_int8(report[3]).value
                    cam.eye = eye
                    cam.target = adsk.core.Point3D.create(0,0,0)
                    cam.upVector = adsk.core.Vector3D.create(0,0,1)
                    
                if (report[0] == 2):
                    rx = report[1]
                    ry = report[2]
                    rz = report[3]

            app.activeViewport.camera = cam
            adsk.doEvents()
            app.activeViewport.refresh()

                 
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        ui.messageBox('Stop addin')
        mouse.close()


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
