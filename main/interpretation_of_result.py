import matplotlib.pyplot as plt
import numpy as np


def autolabel(bar_plot, ax, bar_label):
    """Добавляет на гистограмму числовые значения для столбцов"""
    for idx, rect in enumerate(bar_plot):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                bar_label[idx],
                ha='center', va='bottom', rotation=0)


def create_histogram(data, avg):
    """
    Создает гистограмму для визуализации данных
    :param data: Список с попаданиями толщин в интервалы
    """
    fig, ax = plt.subplots()

    bar_x = [i for i in range(1, len(data) + 1)]
    bar_height = [round(i) for i in data]
    bar_tick_label = [round(i, 3) for i in np.arange(0.025, 0.525, 0.025)]
    bar_label = [round(i) for i in data]

    bar_plot = plt.bar(bar_x, bar_height, tick_label=bar_tick_label)

    autolabel(bar_plot, ax, bar_label)

    ax.annotate(f'Средняя толщина = {avg:.3f} мм', xy=(0, 90))

    plt.ylim(0, 100)
    plt.xlabel('Толщина, мм')
    plt.ylabel('Доля от длины')
    plt.show()


