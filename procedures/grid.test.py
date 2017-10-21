import unittest
from grid import Grid

class GridText(unittest.TestCase):
    def setUp(self):
        self.grid = Grid()

    def test_grids_default_current_cell_is_the_first_cell(self):
        self.assertEqual(self.grid.current_cell, self.grid.get_grid()[0])

if __name__ == '__main__':
    unittest.main()
