from gcode import sendGcode
from datetime import datetime
# from picamera import PiCameraError
# from camera.camera import square_has_plant

retry_seeding_interval = 1209600 # 14 days
watering_interval = 2 #2x per day


def go_home():
    sendGcode('H0;\n')

def turn_off_motors():
    sendGcode('M18;\n')

def go_to(cell):
    # Send Gcode and wait for response
    sendGcode('G00 X' + str(cell.x) + ' Y' + str(cell.y) + ';\n')

def water(seconds):
    sendGcode('P00 S' + str(seconds) + ';\n')

def drop_seed():
    sendGcode('S00 D180 F30;\n')
    sendGcode('S00 D0 F100;\n')

def process_cell(cell):
    now = datetime.now()
    seconds = now.second

    if cell.planted:
        needs_seed = (seconds - cell.planted.second) >= retry_seeding_interval
    else:
        needs_seed = True

    # needs_watering = not cell.watered or (now - cell.watered.seconds) >= watering_interval
    # needs_a_seed = not plant_growing_in_cell and not has_been_planted
    # if not plant_exists and not has_been_planted:
    # if needs_a_seed:
    # try:
    #     cell.occupied = square_has_plant();
    # except PiCameraError:
    #     print ("Camera error", PiCameraError)

    # if needs_seed and not cell.occupied:
    if needs_seed:
        drop_seed()
        cell.set_planted(now)

    # if needs_watering:
    # water(3)
    # cell.set_watered(now)


def patrol(grid):
    go_home()
    while grid.next_cell(): # Will return false if nothing left to go to
        grid.set_current_cell(grid.next_cell())
        current_cell = grid.get_current_cell()
        print(current_cell)
        go_to(current_cell)
        process_cell(current_cell)
    go_home()
    turn_off_motors()
