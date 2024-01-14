from tensorflow import keras
import os
import numpy as np
from imutils.contours import sort_contours

from cv_utils import *
from sympy_utils import *


def run_interference(img_path):

    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
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

    model = keras.models.load_model(
        r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\models\symbol_recognition_9")
    predictions = model.predict(equation_chars)
    labels = sorted(os.listdir(
        r'C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\datasets\dataset'))

    final_string = ""

    for prediction, box in zip(predictions, bounding_boxes):
        x, y, w, h = box

        index = np.argmax(prediction)
        probability = prediction[index]
        label = labels[index]
        final_string += label

        print("[INFO] {} - {:.2f}%".format(label, probability * 100))
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0))
        cv2.putText(img, label, (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

        cv2.imshow("Image", img)
        cv2.waitKey(0)

    print(interpret_equation_string(final_string))