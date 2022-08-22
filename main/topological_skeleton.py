import cv2
import numpy as np


class TopologicalSkeleton:
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

    def __init__(self, image):
        self.source_image = image
        self.skel = None
        self.createEmptySkeleton()
        self.refineSkeleton()

    def createEmptySkeleton(self):
        """Создаёт пустую карту для скелета"""
        self.skel = np.zeros(self.source_image.shape, np.uint8)

    def refineSkeleton(self):
        """Создает скелет на основе исходного изображения"""
        while True:
            open = cv2.morphologyEx(self.source_image, cv2.MORPH_OPEN, self.element)
            temp = cv2.subtract(self.source_image, open)
            eroded = cv2.erode(self.source_image, self.element)
            self.skel = cv2.bitwise_or(self.skel, temp)
            self.source_image = eroded.copy()
            if cv2.countNonZero(self.source_image) == 0:
                break

    def showSkeleton(self):
        """Демонстрирует скелет"""
        temp = self.skel.copy()
        temp[temp == 0] = 254
        temp[temp == 255] = 1
        cv2.imshow("Skeleton", temp)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

