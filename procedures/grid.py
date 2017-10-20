import sqlite3

conn = sqlite3.connect('saladbot.db')
c = conn.cursor()

CELL_SIZE = 30
MAX_X = 330
MAX_Y = 870

class Cell():
    def __init__(self, id, x, y, occupied, planted, watered):
        self.id = id
        self.x = x
        self.y = y
        self.occupied = occupied
        self.planted = planted
        self.watered = watered

        def _update():
            c.execute("UPDATE cells SET occupied = (?), planted = (?), watered = (?) WHERE id = (?)", (self.occupied, self.planted, self.watered, self.id))
            conn.commit()

        def set_planted(planted):
            self.planted = planted
            self._update()

        def set_watered(watered):
            self.watered = watered
            self._update()

        def set_occupied(occupied):
            self.occupied = occupied
            self._update()


class Grid():
    def __init__(self):
        self.grid = []
        try:
            cells = c.execute("SELECT * FROM cells ORDER BY id ASC")
            self.grid = list(map(lambda row: Cell(id=row[0],x=row[1],y=row[2],occupied=row[3],planted=row[4],watered=row[5]), cells))

        except sqlite3.OperationalError:
            c.execute("CREATE TABLE cells (id integer primary key, x integer, y integer, occupied boolean, planted datetime, watered datetime)")

            cells = []
            # Based on boundaries, populate table with cells
            id = 0
            for i in range(0, MAX_Y + CELL_SIZE, CELL_SIZE): # Must be inclusive
                for j in range(0, MAX_X + CELL_SIZE, CELL_SIZE):
                    id = id + 1
                    cell = (id, j, i, False, None, None)
                    cells.append(cell)
                    self.grid.append(Cell(id=id, x=cell[0], y=cell[1], occupied=cell[2], planted=cell[3], watered=cell[4]))

            c.executemany("INSERT INTO cells (id, x, y, occupied, planted, watered) VALUES (?,?,?,?,?,?)", cells)
            conn.commit()
        print(self.grid)
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
        is_advancing_row = ( current_cell.y / CELL_SIZE ) % 2 == 0

        if is_advancing_row:
            if current_cell.x == MAX_X:
                return self.find_cell(x = current_cell.x, y = (current_cell.y + CELL_SIZE)) # Move to next y row
            else:
                return self.find_cell(x = current_cell.x + CELL_SIZE, y = current_cell.y)
        else:
            if current_cell.x == 0:
                return self.find_cell(x = current_cell.x, y = current_cell.y + CELL_SIZE)
            else:
                return self.find_cell(x = current_cell.x - CELL_SIZE, y = current_cell.y)

    def find_cell(self,x,y):
        for cell in self.grid:
            if cell.x == x and cell.y == y:
                return cell
        return False
