import tensorflow as tf
from drawingBoard import DrawingBoard
from recognizer import DigitRecognizer

def main():
    model = tf.keras.models.load_model('models/mnist model')
    digit_recognizer = DigitRecognizer(model)

    test = DrawingBoard(digit_recognizer)
    test.create_board()

    test.main_loop()


if __name__ == '__main__':
    main()
