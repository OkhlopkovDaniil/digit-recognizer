import pygame as pg
from grid import PixelGrid


class DrawingBoard:
    def __init__(self, recognizer):
        '''
        Constructs an empty drawing board

        Parameters: 
            recognizer: DigitRecognizer(or any class that have an implementation of recognize method)
        
        Returns: None
        '''

        pg.init()

        self._width = 28
        self._height = 28
        self._pixel_height = 30
        self._pixel_width = 30

        self.recognizer = recognizer
        self.pixel_grid = PixelGrid(
            self._height, self._width, 
            self._pixel_height, self._pixel_width
        )

        self._board_width = self._width * self._pixel_width
        self._board_height = self._height * self._pixel_height
        self.output_height = 50

        self._line_color = (255, 255, 255)
        self._background_color = (0, 0, 0)

        self._board_window = None
        self.current_output = None

    
    def create_board(self):
        self._board_window = pg.display.set_mode(
            (self._board_width, self._board_height + self.output_height))
        self._board_window.fill(self._background_color)
        pg.display.set_caption('MNIST classifier')
        
        for cell_id in range(1, self._width+1):
            pg.draw.line(
                self._board_window,
                self._line_color, 
                (cell_id*self._pixel_width, 0),
                (cell_id*self._pixel_width, self._board_height)
            )
        
        for cell_id in range(1, self._height+1):
            pg.draw.line(
                self._board_window,
                self._line_color, 
                (0, cell_id*self._pixel_height),
                (self._board_width, cell_id*self._pixel_height)
            )

        self.current_output = self.render_text("Press space when you're done drawing")
        pg.display.update()
    
     
    def render_text(self, text):
        '''
        Renders the passed text and displays it in the special output space below the board

        Parameters: 
            text: string
        
        Returns: None
        '''
        text_background = self._background_color
        text_color = self._line_color

        pos = (0, self._board_height + self.output_height / 3)

        font = pg.font.Font('freesansbold.ttf', 32)
        text_r = font.render(text, True, text_color, text_background)
        self._board_window.blit(text_r, pos)
    

    def erase_text(self):
        '''
        Erases text from the special output space below the board 

        Parameters: None

        Returns: None
        '''
        coords = [
            0,
            self._board_height+1,
            self._board_width,
            self._board_height + self.output_height
        ]

        pg.draw.rect(self._board_window, self._background_color, coords)


    def draw_pixel(self, pixel_row, pixel_col, color):
        '''
        Colors a pixel on the board

        Parameters: 
            pixel_row: int
            pixel_col: int
            color: int
        
        Returns: None
        '''
        rect_coords = [
            pixel_col * self._pixel_width,
            pixel_row * self._pixel_height,
            self._pixel_width,
            self._pixel_height,            
        ]

        pg.draw.rect(self._board_window, color, rect_coords)


    def reset(self):
        '''
        Clears the board

        Parameters: None

        Returns: None
        '''
        self.pixel_grid.clear()
        self.create_board()


    def main_loop(self):
        '''
        Main loop of the game, allows user to draw, reset and 
        use network to recognize the number

        Parameters: None

        Returns: None
        '''
        neighbor_color = 160 / 255
        neighbor_pix_color = (160, 160, 160)

        if self._board_window is not None:
            is_going = True
            while is_going is True:
                events = pg.event.get()

                for event in events:
                    if event.type == pg.QUIT:
                        is_going = False
                    elif event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:
                        self.reset()
                    elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                        guess = self.recognizer.recognize(self.pixel_grid.grid)

                        self.erase_text()
                        self.render_text(f"Model thinks it's {guess}")
                    elif pg.mouse.get_pressed()[0] is True:
                        x, y = pg.mouse.get_pos()

                        if x >= self._board_width or y >= self._board_width:
                            break
                        
                        (pixel_row, pixel_col) = self.pixel_grid.to_grid_pos(x, y)
                        self.pixel_grid.color_pixel(pixel_row, pixel_col, 1)
                        self.draw_pixel(pixel_row, pixel_col, self._line_color)

                        neighbors = self.pixel_grid.pixel_neighbors(pixel_row, pixel_col)
                        for (neighbor_row, neighbor_col) in neighbors:
                            if self.pixel_grid.is_available(neighbor_row, neighbor_col):
                                self.pixel_grid.color_pixel(neighbor_row, neighbor_col, neighbor_color)
                                self.draw_pixel(neighbor_row, neighbor_col, neighbor_pix_color)


                    pg.display.update()


    def __del__(self):
        pg.quit()

