import numpy as np
import sqlite3

conn = sqlite3.connect('saladbot.db')
c = conn.cursor()

CELL_SIZE = 10
MAX_X = 350
MIN_X = 50
MAX_Y = 900
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
            for i in range(0, MAX_Y, CELL_SIZE):
                for j in range(0, MAX_X, CELL_SIZE):
                    cell = (j, i, False, None, None)
                    cells.append(cell)
                    self.grid.append(cell)

            c.executemany("INSERT INTO cells (x, y, occupied, planted, watered) VALUES (?,?,?,?,?)", cells)
            conn.commit()

        self.grid.current_cell = self.grid[0]

    def get_grid(self):
        return self.grid

    def next_cell(self):
        current_cell = self.grid.current_cell
        is_advancing_row = ( current_cell.y / 10 ) % 2 == 0

        if is_advancing_row:
            if current_cell.x == MAX_X:
                return self.find_cell(x = current_cell.x, y = current_cell.y + 1) # Move to next y row
            else:
                return self.find_cell(x = current_cell.x + 1, y = current_cell.y)
        else:
            if current_cell.x == 0:
                return self.find_cell(x = current_cell.x, y = current_cell.y + 1)
            else:
                return self.find_cell(x = current_cell.x - 1, y = current_cell.y)

    def find_cell(self,x,y):
        for cell in self.grid:
            if cell.x == x and cell.y == y
                return cell
        return False
