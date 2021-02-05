import pygame as pg
import numpy as np

from grid import PixelGrid

class DrawingBoard:
    def __init__(self, model):
        pg.init()

        self._width = 28
        self._height = 28
        self._pixel_height = 30
        self._pixel_width = 30

        self._model = model
        self.pixel_grid = PixelGrid(
            self._height, self._width, 
            self._pixel_height, self._pixel_width
        )

        self._output_width = 170
        self._board_width = self._width * self._pixel_width
        self._board_height = self._height * self._pixel_height
        
        self._buttons_x_pos = self._board_width + self._output_width / 10
        self._class_button_y_pos  =  self._board_height / 10
        self._reset_button_y_pos = self._board_height / 2.5
        self._output_window_y_pos = self._board_height / 1.3

        self._buttons_width = self._output_width / 1.2
        self._buttons_height = self._output_width / 1.2

        self._empty_pixel = 0
        self._line_color = (0, 0, 0)
        self._buttons_color = (0, 0, 0)
        self._background_color = (255, 255, 255)

        self._board_window = None

    
    def create_board(self):
        self._board_window = pg.display.set_mode(
            (self._board_width + self._output_width, self._board_height))
        self._board_window.fill(self._background_color)
        pg.display.set_caption('MNIST classifier')
        
        for cell_id in range(1, self._width+1):
            pg.draw.line(
                self._board_window,
                self._line_color, 
                (cell_id*self._pixel_width, 0),
                (cell_id*self._pixel_width, self._board_height)
            )
        
        for cell_id in range(1, self._height):
            pg.draw.line(
                self._board_window,
                self._line_color, 
                (0, cell_id*self._pixel_height),
                (self._board_width, cell_id*self._pixel_height)
            )
        
        class_button_pos = [
            self._buttons_x_pos,
            self._class_button_y_pos,
            self._buttons_width,
            self._buttons_height
        ]

        reset_button_pos = [
            self._buttons_x_pos,
            self._reset_button_y_pos,
            self._buttons_width,
            self._buttons_height,
        ]

        output_window_pos = [
            self._buttons_x_pos,
            self._output_window_y_pos,
            self._buttons_width,
            self._buttons_height,
        ]

        pg.draw.rect(self._board_window, self._buttons_color, class_button_pos)
        pg.draw.rect(self._board_window, self._buttons_color, reset_button_pos)
        pg.draw.rect(self._board_window, self._buttons_color, output_window_pos, 2)

        text_color = (255, 255, 255)
        text_offset_x = 0.1*self._buttons_width
        text_offset_y =  0.3*self._buttons_height

        button_font = pg.font.SysFont("Corbel", 40)
        class_text = button_font.render('classify', True, text_color)
        reset_text = button_font.render('reset', True, text_color)

        self._board_window.blit(
            class_text, 
            (self._buttons_x_pos + text_offset_x, self._class_button_y_pos + text_offset_y)
        ) 
        self._board_window.blit(
            reset_text, 
            (self._buttons_x_pos + text_offset_x, self._reset_button_y_pos + text_offset_y)
        ) 

        pg.display.update()
     

    def draw_pixel(self, pixel_row, pixel_col, color):
        rect_coords = [
            pixel_col * self._pixel_width,
            pixel_row * self._pixel_height,
            self._pixel_width,
            self._pixel_height,            
        ]

        pg.draw.rect(self._board_window, color, rect_coords)


    def classify_digit(self):
        prediction = self._model.predict(np.array([self.pixel_grid.grid]))
        return np.argmax(prediction)


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
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        x, y = pg.mouse.get_pos()

                        if (self._buttons_x_pos <= x <= self._buttons_x_pos + self._buttons_width and
                            self._class_button_y_pos <= y <= self._class_button_y_pos + self._buttons_height):
                            digit = self.classify_digit()
                            self.display_digit(digit)
                        elif (self._buttons_x_pos <= x <= self._buttons_x_pos + self._buttons_width and
                            self._reset_button_y_pos <= y <= self._reset_button_y_pos + self._buttons_height):
                            self.reset()
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

