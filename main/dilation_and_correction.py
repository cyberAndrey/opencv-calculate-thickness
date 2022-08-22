import math

import cv2
import numpy as np
from statistics import mean


def get_brightness_inside_fiber(source, mask):
    """Считает среднюю яркость внутри волокон"""
    return source[mask == 0].mean()


def get_brightness_outside_fiber(source, mask):
    """Считает среднюю яркость снаружи волокон"""
    temp = source.copy()
    temp[mask != 0] = 0
    temp[mask == 0] = 255
    return get_brightness_inside_fiber(source, temp)


def draw_circle(mask, center, radius):
    """
    Рисует окружность
     :param mask: Изображение, на котором будет окружность
     :param center: Координаты центра окружности
    :param radius: Радиус окружности
    :return: Входное изображение с нарисованной окружностью
    """
    return cv2.circle(mask, center, radius, (100, 100, 100), thickness=-1)


class DilationAndCorrection:
    window_name = "DILATION"

    def __init__(self, source, dil_mask, level, scale):
        self.source = source
        self.scale = scale
        self.inside = None
        self.outside = None
        self.dil_mask = dil_mask
        self.dilatation(level)
        self.map_with_accuracy = self.dil_mask.copy()
        self.calculate_subpixel_accuracy()

    def dilatation(self, val):
        """
        Выполняет диляцию маски на указанное количество пикселей
        :param val: 1 пиксель для получения границ
        """
        dilation_shape = cv2.MORPH_CROSS
        source_mask = self.dil_mask.copy()
        element = cv2.getStructuringElement(dilation_shape, (2 * val + 1, 2 * val + 1), (val, val))
        dilatation_dst = cv2.dilate(self.dil_mask, element)
        self.inside = get_brightness_inside_fiber(self.source, self.dil_mask)
        self.dil_mask = dilatation_dst
        self.outside = get_brightness_outside_fiber(self.source, self.dil_mask)
        self.dil_mask[source_mask == 255] = 0

    def calculate_subpixel_accuracy(self):
        """
        Считает субпиксельную толщину для пикселей границ
        :return: self.map_with_accuracy будет заполнена значениями толщин в каждом пикселе границ
        """
        indexes_tuple = np.nonzero(self.dil_mask)
        indexes = np.transpose(indexes_tuple)
        self.map_with_accuracy = self.map_with_accuracy.astype(float)
        for i in indexes:
            self.map_with_accuracy[i[0]][i[1]] = math.fabs(self.source[i[0]][i[1]] - self.outside) \
                                                 / (self.inside - self.outside) * self.scale

    def get_correction(self, distances, indexes):
        """
        Для каждого пикселя скелета рассчитывает дополнительную субпиксельную толщину волокна
        :param distances: Карта преобрания distance transform для получения радиуса окружности
        :param indexes: Индексы пикселей топологического скелета.
        Тот же порядок, что и при вычислении толщины методом get_thickness
        :return: Спискок дополнительных толщин волокон для каждого пикселя скелета
        """
        correction = []
        for i in indexes:
            tmp = np.zeros(self.dil_mask.shape, np.uint8)
            tmp = draw_circle(tmp, (i[1], i[0]), round(distances[i[0]][i[1]]) + 1)
            tmp_2 = list(self.map_with_accuracy[tmp != 0])
            tmp_2 = [i for i in tmp_2 if i > 0]
            if len(tmp_2) > 0:
                correction.append(mean(tmp_2) * 2)
            else:
                correction.append(0)
        return correction
