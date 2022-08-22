import cv2
from topological_skeleton import TopologicalSkeleton
from calculate_thickness import get_thickness
from remove_stains import RemoveStains
from cleansing import MorphologicalClosure
from dilation_and_correction import DilationAndCorrection
from config import Config as cfg


def distance_transform(mask):
    out = cv2.distanceTransform(mask, cv2.DIST_L2, 3)
    return out


def process(path, scope):
    adaptive, source = adaptiveThreshold(path)

    rmv = RemoveStains(adaptive, scope)
    rmv = rmv.filter()

    dst = MorphologicalClosure(rmv, cfg.closureConst)

    skel = TopologicalSkeleton(dst.image.copy())

    distances = distance_transform(dst.image)

    thickness, indexes = get_thickness(distances, skel.skel, scope)

    if cfg.correction:
        dilation = DilationAndCorrection(source.copy(), dst.image.copy(), 1, scope)
        correction = dilation.get_correction(distances, indexes)
        thickness = map(sum, zip(thickness, correction))

    return thickness


def adaptiveThreshold(img):
    src = cv2.imread(img, 0)
    th = cv2.adaptiveThreshold(src, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
                                    cfg.thresholdWindow, cfg.thresholdConst)
    return th, src
