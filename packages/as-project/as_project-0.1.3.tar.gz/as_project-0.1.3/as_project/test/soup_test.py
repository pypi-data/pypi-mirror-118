from as_project import alphabet_soup, grid_slice
import unittest
import numpy as np
from contextlib import redirect_stdout
import io

class SoupTest(unittest.TestCase):
    # test grid_slice function
    print('grid slice test')

    def test_grid_slice(self):
        grid = np.array([['A', 'B', 'C'], ['D', 'E', 'F'],
            ['G', 'H', 'I'], ['J', 'K', 'L']])
        g = grid_slice(grid, [1, 0], [3, 2], [1, 1])
        self.assertEqual(g, 'DHL')
        g = grid_slice(grid, [2, 0], [0, 2], [-1, 1])
        self.assertEqual(g, 'GEC')
        g = grid_slice(grid, [2, 2], [2, 1], [0, -1])
        self.assertEqual(g, 'IH')

    # test alphabet soup
    print('alphabet soup test')
    def test_alphabet_soup(self):
        # Get correct output from file
        with open("test.out") as f:
            correct_output = f.read()
        f.close()

        # alphabet_soup outputs to console, redirect to capture
        f = io.StringIO()
        with redirect_stdout(f):
            print('direction test')
            alphabet_soup('test1.txt')

            print('\ngiven test')
            alphabet_soup('test2.txt')

            print('\nwhite space test')
            alphabet_soup('test3.txt')

            print('\nrectangular grid test')
            alphabet_soup('test4.txt')

            print('\nsingle letter word test')
            alphabet_soup('test5.txt')

        self.assertEqual(f.getvalue(), correct_output)
        f.close()

if __name__ == '__main__':
    unittest.main()



