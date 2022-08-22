import cv2


class RemoveStains:

    def __init__(self, image, scope):
        self.image = image
        self.connectivity = 1
        self.scope = scope

    def filter(self):
        """Выделяет все связанные компоненты и отсеивает те, чья площидь меньше необходимой"""
        mask = self.image.copy()
        mask[mask == 255] = 0
        output = cv2.connectedComponentsWithStats(
            self.image, self.connectivity, cv2.CV_32S)
        (numLabels, labels, stats, centroids) = output
        for i in range(1, numLabels):
            area = stats[i, cv2.CC_STAT_AREA]
            if area > 100 * self.scope * 100:
                component_mask = (labels == i).astype("uint8") * 255
                mask[component_mask == 255] = 255
        return mask
