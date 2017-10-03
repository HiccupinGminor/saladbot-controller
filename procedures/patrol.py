from gcode import sendGcode
import time
# from camera.camera import square_has_plant

def go_home():
    sendGcode('G00 X0 Y0;\n')

def go_to(cell):
    # Send Gcode and wait for response
    sendGcode('G00 X' + str(cell[1]) + ' Y' + str(cell[2]) + ';\n')

def patrol(grid):
    go_home()
    time.sleep(5)
    
    while grid.next_cell(): # Will return false if nothing left to go to
        print(grid.next_cell())
        grid.set_current_cell(grid.next_cell())
        go_to(grid.get_current_cell())
