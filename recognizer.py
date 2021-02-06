import numpy as np
import tensorflow as tf


class DigitRecognizer():
    def __init__(self, model):
        '''
        Construct the recognizer

        Parameters: 
            model: any model that have predict method, which accepts numpy array
        Returns: None
        '''
        self.model = model
    

    def recognize(self, pixel_digit):
        '''
        Recognizes the passed digit

        Parameters:
            pixel_digit: numpy array, which represent the digit
        Returns: int digit
        '''
        prediction = self.model.predict(np.array([pixel_digit]))
        return np.argmax(prediction)