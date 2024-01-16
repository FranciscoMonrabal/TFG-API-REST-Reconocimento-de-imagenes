import os

from tensorflow import keras
import cv2
import imutils
from imutils.contours import sort_contours
import math
import numpy as np
from sympy.core.sympify import sympify
from sympy import Eq, solve
from sympy.abc import x as X

# https://stackoverflow.com/questions/22356494/solve-2-sides-of-equation-with-sympy
# In the case of boxes colliding, pick the biggest one


def convert_point_to_point_to_xyhw(box):
    return box[0][0], box[0][1], box[1][0] - box[0][0], box[1][1] - box[0][1]


def convert_xyhw_to_point_to_point(box):
    return [box[0], box[1]], [box[0] + box[2], box[1] + box[3]]


def overlap(source, target):

    ret = True
    tl1, br1 = source
    tl2, br2 = target

    # checks
    if tl1[0] >= br2[0] or tl2[0] >= br1[0]:
        ret = False

    if tl1[1] >= br2[1] or tl2[1] >= br1[1]:
        ret = False

    return ret


def merge_boxes(source, target):
    ret = []
    tl1, br1 = source
    tl2, br2 = target

    ret.append([min(tl1[0], tl2[0]), min(tl1[1], tl1[1])])
    ret.append([max(br1[0], br2[0]), max(br1[1], br2[1])])

    return ret


def transform_points_list_to_boxes_tuple(blist):

    ret = []

    for box in blist:
        ret.append(convert_point_to_point_to_xyhw(box))

    return tuple(ret)


def transform_boxes_tuple_to_points_list(tuple):

    ret = []

    for box in tuple:
        ret.append(convert_xyhw_to_point_to_point(box))

    return ret


def group_overlapped_boxes(input_list):

    ret = []
    boxes = transform_boxes_tuple_to_points_list(input_list)
    prev_box = [[0, 0], [0, 0]]

    for box in boxes:
        if overlap(prev_box, box):
            prev_box = merge_boxes(prev_box, box)

            if box == boxes[-1]:
                ret.append(prev_box)
        else:
            ret.append(prev_box)
            prev_box = box

            # If we are at the end and the two boxes are not overlapped
            if box == boxes[-1]:
                ret.append(box)

    # Remove the first element that we added for the comparison
    ret.remove([[0, 0], [0, 0]])

    return transform_points_list_to_boxes_tuple(ret)


def remove_small_boxes(b_list, min_w=15, min_h=15):

    ret = []

    for box in b_list:
        if box[2] >= min_w or box[3] >= min_h:
            ret.append(box)

    return ret


def replace_posible_equals(equation_string):

    ret = equation_string.replace("--", "=")
    ret = ret.replace("-=", "=")
    ret = ret.replace("==", "=")
    if len(ret.split("=")) > 2:
        raise TypeError("Multiple equal signs, or -- detected")

    return ret


def add_products(equation_string):

    ret = ""
    prev_char = ""

    for char in equation_string:
        if char == "(":
            if prev_char.isnumeric() or prev_char == "x" or prev_char == "(":
                ret += r"*"

        if char == "x":
            if prev_char.isnumeric():
                ret += r"*"

        if prev_char == "x":
            if char.isnumeric():
                ret += r"*"

        if prev_char == ")":
            if char.isnumeric() or char == "x":
                ret += r"*"

        ret += char
        prev_char = char

    return ret


def interpret_equation_string(equation_string):

    equation_string = replace_posible_equals(equation_string)
    equation_string = add_products(equation_string)
    print(f"Final equation: {equation_string}")

    equation_splited = equation_string.split("=")
    left_eq = sympify(equation_splited[0])
    right_eq = sympify(equation_splited[1])
    eqn = Eq(left_eq, right_eq)

    return solve(eqn, X)


def adjust_padding(distance):

    ret = (0, 0)
    padding_side = distance / 2

    if (padding_side - math.trunc(padding_side)) == 0:
        new_dis = distance / 2
        ret = (int(new_dis), int(new_dis))
    else:
        new_dis = distance / 2
        ret = (int(new_dis), int(new_dis+1))

    return ret


def main():

    img = cv2.imread(
        r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\test_images\numbers.jpeg"
        , cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(img, (5, 5), 0)

    edged = cv2.Canny(blurred, 30, 150)
    dilated = cv2.dilate(edged, (1, 1), iterations=2)
    contours = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours, bounding_boxes = sort_contours(contours, method="left-to-right")

    print("Pre group: ")
    print(f"Size: {len(bounding_boxes)}")
    print(bounding_boxes)
    print("===========================================")
    bounding_boxes = group_overlapped_boxes(bounding_boxes)
    print("Post group: ")
    print(f"Size: {len(bounding_boxes)}")
    print(bounding_boxes)
    print("===========================================")
    print("Pre removal small: ")
    print(f"Size: {len(bounding_boxes)}")
    print(bounding_boxes)
    print("===========================================")
    bounding_boxes = remove_small_boxes(bounding_boxes)
    print("Post removal small: ")
    print(f"Size: {len(bounding_boxes)}")
    print(bounding_boxes)

    equation_chars = []
    for box in bounding_boxes:
        (x, y, w, h) = box

        roi = img[y:y + h, x:x + w]
        roi_binary = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        (height, width) = roi_binary.shape

        if height > width:
            roi_binary = imutils.resize(roi_binary, height=45, inter=cv2.INTER_NEAREST)
            padding = adjust_padding(int(45 - roi_binary.shape[1]))
            print(f"{roi_binary.shape} | {padding} | {width} | {height}")
            roi_binary = cv2.copyMakeBorder(roi_binary, top=0, bottom=0, left=padding[0], right=padding[1],
                                            borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255))
        else:
            roi_binary = imutils.resize(roi_binary, width=45, inter=cv2.INTER_NEAREST)
            padding = adjust_padding(45 - roi_binary.shape[0])
            print(f"{roi_binary.shape} | {padding}")
            roi_binary = cv2.copyMakeBorder(roi_binary, left=0, right=0, top=padding[0], bottom=padding[1],
                                            borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255))

        equation_chars.append(roi_binary)

    index = 0
    for char in equation_chars:
        cv2.imshow(f"{index}", char)
        index += 1

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    equation_chars = np.array([c for c in equation_chars], dtype="float32")

    print(equation_chars)
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

        print("[INFO] {} - {:.2f}%".format(label, probability*100))
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0))
        cv2.putText(img, label, (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

        cv2.imshow("Image", img)
        cv2.waitKey(0)

    print(interpret_equation_string(final_string))


if __name__ == "__main__":
    main()


