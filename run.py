import tensorflow as tf
from DrawingBoard import DrawingBoard


def main():
    model = tf.keras.models.load_model('models/mnist model')
    test = DrawingBoard(model)
    test.create_board()
    test.main_loop()


if __name__ == '__main__':
    main()
