from gcode import sendGcode
import time
from camera.camera import square_has_plant

def go_home():
    sendGcode('G00 X0 Y0;\n')

def go_to(cell):
    # Send Gcode and wait for response
    sendGcode('G00 X' + str(cell.x) + ' Y' + str(cell.y) + ';\n')

def water(seconds):
    sendGcode('P00 S' + str(seconds) + ';\n')

def drop_seed():
    sendGcode('S00 D180 F30;\n')
    sendGcode('S00 D0 F100;\n')

def process_cell(cell):
    print("PLANT EXISTS:", square_has_plant())


def patrol(grid):
    go_home()
    while grid.next_cell(): # Will return false if nothing left to go to
        grid.set_current_cell(grid.next_cell())
        current_cell = grid.get_current_cell()
        print(current_cell)
        go_to(current_cell)
        process_cell(current_cell)
