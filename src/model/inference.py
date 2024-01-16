from tensorflow import keras
import os
import numpy as np
from imutils.contours import sort_contours

from cv_utils import *
from sympy_utils import *


def run_interference(config):

    img = cv2.imread(config.get_image_path(), cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(img, (5, 5), 0)

    edged = cv2.Canny(blurred, 30, 150)
    dilated = cv2.dilate(edged, (1, 1), iterations=2)
    contours = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours, bounding_boxes = sort_contours(contours, method="left-to-right")

    bounding_boxes = group_overlapped_boxes(bounding_boxes)
    bounding_boxes = remove_small_boxes(bounding_boxes)
    equation_chars = trim_character_rois(bounding_boxes, img)
    equation_chars = np.array([c for c in equation_chars], dtype="float32")

    model = keras.models.load_model(config.get_model_path())
    predictions = model.predict(equation_chars)
    labels = sorted(os.listdir(config.get_dataset_path()))

    final_string, img = analize_equation_and_image(predictions, bounding_boxes, img, labels)
    result = interpret_equation_string(final_string)
    write_result(img, result, config.get_final_image_path())

    # Implement in case the equation cant be solved

    return result, config.get_final_image_path()
