from dataset_iterator import DatasetIterator
import cv2 as cv
import numpy as np
import os


def main():

    di = DatasetIterator(r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\dataset",
                         r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\dataset_augmented",
                         create_dialated_versions)


def create_dialated_versions(image_path):
    dilatate_image(image_path, (1, 1))
    dilatate_image(image_path, (3, 3))
    dilatate_image(image_path, (5, 5))


def dilatate_image(image_path, matrix_size):
    img = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    kernel = np.ones(matrix_size, np.uint8)
    return cv.dilate(img, kernel, iterations=1)



