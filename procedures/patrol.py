from gcode import sendGcode
from datetime import datetime
from camera.camera import square_has_plant

retry_seeding_interval = 7 #days
watering_frequency = 2 #2x per day


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
    # plant_exists = cell.occupied or square_has_plant()
    now = datetime.now()
    # has_been_planted = (now - cell.planted) >= retry_seeding_interval
    needs_watering = not cell.watered or (now - cell.watered) >= watering_frequency

    # if not plant_exists and not has_been_planted:
    drop_seed()

    if needs_watering:
        water(5)


def patrol(grid):
    go_home()
    while grid.next_cell(): # Will return false if nothing left to go to
        grid.set_current_cell(grid.next_cell())
        current_cell = grid.get_current_cell()
        print(current_cell)
        go_to(current_cell)
        process_cell(current_cell)
