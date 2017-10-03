import sqlite3

conn = sqlite3.connect('saladbot.db')
c = conn.cursor()

CELL_SIZE = 10
MAX_X = 330
MIN_X = 50
MAX_Y = 870
MIN_Y = 50

class Grid():
    def __init__(self):
        self.grid = []
        try:
            cells = c.execute("SELECT * FROM cells ORDER BY id ASC")
            self.grid = cells.fetchall()
        except sqlite3.OperationalError:
            c.execute("CREATE TABLE cells (id integer primary key, x integer, y integer, occupied boolean, planted datetime, watered datetime)")

            cells = []
            # Based on boundaries, populate table with cells
            for i in range(0, MAX_Y + CELL_SIZE, CELL_SIZE): # Must be inclusive
                for j in range(0, MAX_X + CELL_SIZE, CELL_SIZE):
                    cell = (j, i, False, None, None)
                    cells.append(cell)
                    self.grid.append(cell)

            c.executemany("INSERT INTO cells (x, y, occupied, planted, watered) VALUES (?,?,?,?,?)", cells)
            conn.commit()

        self.current_cell = self.grid[0]

    def get_grid(self):
        return self.grid

    def set_current_cell(self, cell):
        if cell:
            self.current_cell = cell
        else:
            self.current_cell = self.find_cell(0,0) # Default to home cell

    def get_current_cell(self):
        return self.current_cell

    def next_cell(self):
        current_cell = self.current_cell
        is_advancing_row = ( current_cell[2] / 10 ) % 2 == 0

        if is_advancing_row:
            if current_cell[1] == MAX_X:
                return self.find_cell(x = current_cell[1], y = current_cell[2] + CELL_SIZE) # Move to next y row
            else:
                return self.find_cell(x = current_cell[1] + CELL_SIZE, y = current_cell[2])
        else:
            if current_cell[1] == 0:
                return self.find_cell(x = current_cell[1], y = current_cell[2] + CELL_SIZE)
            else:
                return self.find_cell(x = current_cell[1] - CELL_SIZE, y = current_cell[2])

    def find_cell(self,x,y):
        for cell in self.grid:
            if cell[1] == x and cell[2] == y:
                return cell
        return False
