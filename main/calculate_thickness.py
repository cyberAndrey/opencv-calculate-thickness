from statistics import mean
from functools import reduce
import numpy as np


def get_thickness(distances, skeleton, scale):
    """
    Считает толщины волокон в кажом пикселе топологического скелета
    :param distances: карта преобразования distance transform
    :param skeleton: карта преобразования Топологический скелет
    :param scale: масштаб изображения
    :return:
    thickness: список толщин. Длина равна длине скелета
    indexes: индексы пикселей скелета, по которым происходили вычисления
    """
    thickness = []
    indexes_tuple = np.nonzero(skeleton)
    indexes = np.transpose(indexes_tuple)
    for i in indexes:
        thickness.append((distances[i[0]][i[1]] * 2 - 1) * scale)
    return thickness, indexes


def distribute_thickness(thickness):
    """
    Распределение точек толщин по интервалам
    :param thickness: Список толщин
    :return:
    distribution: количество попаданий толщин в интервалы
    mean(thickness): среднее значение толщины
    """
    distribution = [reduce(lambda acc, x: acc + (1 if i > x > i - 0.025 else 0), thickness, 0)
                    for i in np.arange(0.025, 0.525, 0.025)]
    all_values = sum(distribution)
    distribution = [i / all_values * 100 for i in distribution]
    return distribution, mean(thickness)
