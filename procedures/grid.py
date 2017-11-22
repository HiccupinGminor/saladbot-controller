import sqlite3

conn = sqlite3.connect('saladbot.db', detect_types=sqlite3.PARSE_DECLTYPES)
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

    def _update(self):
        print("UPDATE CALLED")
        c.execute("UPDATE cells SET occupied = (?), planted = (?), watered = (?) WHERE id = (?)", (self.occupied, self.planted, self.watered, self.id))
        conn.commit()

    def set_planted(self, planted):
        self.planted = planted
        self._update()

    def set_watered(self, watered):
        self.watered = watered
        self._update()

    def set_occupied(self, occupied):
        self.occupied = occupied
        self._update()


class Grid():
    def __init__(self):
        self.grid = []
        try:
            cells = c.execute("SELECT * FROM cells ORDER BY id ASC")
            self.grid = list(map(lambda row: Cell(id=row[0],x=row[1],y=row[2],occupied=row[3],planted=row[4],watered=row[5]), cells))

        except sqlite3.OperationalError:
            c.execute("CREATE TABLE cells (id integer primary key, x integer, y integer, occupied boolean, planted timestamp, watered timestamp)")

            cells = []
            # Based on boundaries, populate table with cells
            id = 0
            for i in range(0, MAX_Y + CELL_SIZE, CELL_SIZE): # Must be inclusive
                for j in range(0, MAX_X + CELL_SIZE, CELL_SIZE):
                    id = id + 1
                    cell = (id, j, i, False, None, None)
                    cells.append(cell)
                    self.grid.append(Cell(id=id, x=cell[1], y=cell[2], occupied=cell[3], planted=cell[4], watered=cell[5]))

            c.executemany("INSERT INTO cells (id, x, y, occupied, planted, watered) VALUES (?,?,?,?,?,?)", cells)
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
