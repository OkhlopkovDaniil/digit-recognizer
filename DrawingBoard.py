import pygame as pg
from grid import PixelGrid

class DrawingBoard:
    def __init__(self, recognizer):
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

        self._line_color = (0, 0, 0)
        self._background_color = (255, 255, 255)

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
        text_background = self._background_color
        text_color = self._line_color

        pos = (0, self._board_height + self.output_height / 3)

        font = pg.font.Font('freesansbold.ttf', 32)
        text_r = font.render(text, True, text_color, text_background)
        self._board_window.blit(text_r, pos)

        return text_r
    

    def erase_text(self):
        coords = [
            0,
            self._board_height+1,
            self._board_width,
            self._board_height + self.output_height
        ]

        pg.draw.rect(self._board_window, self._background_color, coords)


    def draw_pixel(self, pixel_row, pixel_col, color):
        rect_coords = [
            pixel_col * self._pixel_width,
            pixel_row * self._pixel_height,
            self._pixel_width,
            self._pixel_height,            
        ]

        pg.draw.rect(self._board_window, color, rect_coords)


    def display_digit(self, digit):
        digit_color = (0, 0, 0)
        digit_font = pg.font.SysFont("Corbel", 150)
        digit_text = digit_font.render(str(digit), True, digit_color)

        self._board_window.blit(
            digit_text,
            (self._buttons_x_pos + 45, self._output_window_y_pos + 30)
        ) 
        pg.display.update()


    def reset(self):
        self.pixel_grid.clear()
        self.create_board()


    def main_loop(self):
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
                        if self.pixel_grid.color_pixel(pixel_row, pixel_col, 255):
                            self.draw_pixel(pixel_row, pixel_col, self._line_color)

                    pg.display.update()


    def __del__(self):
        pg.quit()

