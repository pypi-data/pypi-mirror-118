import numpy as np

# Extract a 'slice' from the grid in any direction including diagonal
def grid_slice(grid, start, end, sign):
    gs = ''
    # check if slice end point is within the grid; else return empty string
    if (end[0] >= 0 and end[0] < grid.shape[0] and end[1] >= 0 and end[1] <
        grid.shape[1]):
        index = start.copy()
        while index[0] != end[0] or index[1] != end[1]:
            gs += grid[index[0], index[1]]
            index[0] += sign[0]
            index[1] += sign[1]
        gs += grid[end[0], end[1]]
    return gs

# Solve a word search puzzle given by the file 'filename'
def alphabet_soup(filename):
    f = open(filename)
    # read grid size
    line = f.readline()
    height, width = [int(y) for y in line.split('x')]

    # read the grid into an array
    grid = np.empty((height, width), dtype=str)
    for row in range(height):
        line = f.readline()
        line = line.split(' ')
        grid[row, :] = line

    # read the words to find and search grid
    for line in f:
        # remove all whitespace and end-of-line from words, save original
        # word to print at end
        original_word = line.strip()
        w = "".join(original_word.split())

        s = len(w)

        # find all locations in the grid equal to first letter of the word
        loc = np.where(grid == w[0])
        loc = [list(k) for k in zip(loc[0], loc[1])]

        for start in loc:
            # look in each of the eight directions around this location
            # starting at upper left and moving clockwise
            direction = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0],
                [1, -1], [0, -1]]
            
            for d in direction:
                # get a candidate word from the grid starting at first
                # letter location and ending at the length of the word
                # in the desired direction
                end = [d[0] * (s - 1) + start[0], d[1] * (s - 1) + start[1]]
                test_word = grid_slice(grid, start, end, d)
                if test_word == w:
                    # found the word, print output and move on to next word
                    print('{} {}:{} {}:{}'.format(original_word, start[0],
                        start[1], end[0], end[1]))
                    break
    f.close()

