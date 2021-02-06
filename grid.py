import numpy as np

class PixelGrid:
    def __init__(self, height, width, pixel_height, pixel_width, empty_cell=0):
        self.height = height
        self.width = width

        self.empty = empty_cell
        self.grid = np.full( 
            (self.height, self.width), 
            empty_cell, 
            dtype=np.float32
        )

        self.pixel_width = pixel_width
        self.pixel_height = pixel_height
    

    def is_available(self, row, column):
        if row > self.height or column > self.width:
            return False
        
        return self.grid[row][column] == self.empty
    

    def color_pixel(self, row, column, color):
        if row > self.height or column > self.width:
            return False

        self.grid[row][column] = color
        return True


    def pixel_neighbors(self, pixel_row, pixel_column):
        neighbors = list()

        if pixel_row + 1 < self.height:
            neighbors.append((pixel_row+1, pixel_column))

        if pixel_row - 1 >= 0:
            neighbors.append((pixel_row-1, pixel_column)) 

        if pixel_column - 1 >= 0:
            neighbors.append((pixel_row, pixel_column-1)) 

        if pixel_column + 1 < self.width:
            neighbors.append((pixel_row, pixel_column+1))

        return neighbors
    

    def to_grid_pos(self, x, y):
        row = y // self.pixel_height
        column = x // self.pixel_width

        return (row, column)


    def clear(self):
        for pixel_row in range(self.grid.shape[0]):
            for pixel_column in range(self.grid.shape[1]):
                self.grid[pixel_row][pixel_column] = self.empty



    def __getitem__(self, row):
        return self.grid[row]


    def __len__(self):
        return len(self.grid)


