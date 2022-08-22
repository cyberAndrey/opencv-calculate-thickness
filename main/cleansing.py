import cv2
import numpy as np


class MorphologicalClosure:

    def __init__(self, image, value):
        """
        :param image: Исходное изображение
        :param value: Размер ядра для операции
        """
        self.image = image
        self.close(value)

    def close(self, r):
        """
                Применяет к изображению метод морфологического закрытия
                :param r: размер ядра для операции
                :return: меняет изображение self.image
                """
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (r, r))
        closing = cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, kernel, iterations=1)
        self.image = closing
