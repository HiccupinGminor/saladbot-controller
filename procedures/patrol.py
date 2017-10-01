from gcode import sendGcode
from camera.camera import square_has_plant

def goHome():
    sendGcode('G00 X0 Y0;')

def patrol(grid):
    goHome()

    while grid.nextCell(): # Will return false if nothing left to go to
        goTo(grid.nextCell())
