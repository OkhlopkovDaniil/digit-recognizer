import tensorflow as tf
import pygame as pg

from drawing_board import DrawingBoard
from recognizer import DigitRecognizer

def main():
    pg.init()

    model = tf.keras.models.load_model('models/mnist model')
    digit_recognizer = DigitRecognizer(model)

    test = DrawingBoard(digit_recognizer)
    test.create_board()

    test.main_loop()
    
    pg.quit()


if __name__ == '__main__':
    main()
