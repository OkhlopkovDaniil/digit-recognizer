import numpy as np
import tensorflow as tf


class DigitRecognizer():
    def __init__(self, model):
        self.model = model
    

    def recognize(self, pixel_digit):
        prediction = self.model.predict(np.array([pixel_digit]))
        return np.argmax(prediction)