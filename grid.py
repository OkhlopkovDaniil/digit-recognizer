import numpy as np

class PixelGrid:
    def __init__(self, height, width, pixel_height, pixel_width, empty_cell=0):
        '''
        Constructs the empty grid 

        Parameters:
            height: int, the height of a grid
            width: int, the width of a grid
            pixel_height: int, the height of one pixel in a grid
            pixel_width: int, the width of one pixel in a grid
            empty_cell: int(optional), a cell which is considered empty by a grid
        
        Returns: None
        '''
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
        '''
        Check whether or not the position in a grid is available

        Parameters:
            row: int
            column: int
        
        Returns: None
        '''
        if row > self.height or column > self.width:
            return False
        
        return self.grid[row][column] == self.empty
    

    def color_pixel(self, row, column, color):
        '''
        Sets the specified position in the grid to the passed color

        Parameters:
            row: int
            column: int
            color: int from 0 to 255
        
        Returns: bool
        '''
        if row > self.height or column > self.width:
            return False

        self.grid[row][column] = color
        return True


    def pixel_neighbors(self, pixel_row, pixel_column):
        '''
        Find all the neighbors of a given position

        Parameters:
            pixel_row: int
            pixel_column: int
        
        Returns: tuple list, the first value of a tupe is a row, the second one is a column
        '''
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
        '''
        Converts screen coordinates to grid position

        Parameters:
            x: int, x position on a screen
            y: int, y position on a screen
        
        Returns: tuple, the first value is a row, the second value is a column
        '''
        row = y // self.pixel_height
        column = x // self.pixel_width

        return (row, column)


    def clear(self):
        '''
        Sets all the values in a grid to empty

        Parameters: None

        Returns: None
        '''
        for pixel_row in range(self.grid.shape[0]):
            for pixel_column in range(self.grid.shape[1]):
                self.grid[pixel_row][pixel_column] = self.empty



    def __getitem__(self, row):
        return self.grid[row]


    def __len__(self):
        return len(self.grid)


