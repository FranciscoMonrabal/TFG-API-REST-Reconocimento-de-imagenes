from dataset_iterator import DatasetIterator
import cv2 as cv
import numpy as np
import os


def main():

    di = DatasetIterator(
        r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\datasets\dataset",
        r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\datasets\dataset_augmented",
        dilate_image, False, kernel_size=(1, 1))
    di.execute()

    di.args = {"kernel_size": (3, 3)}
    di.execute()

    di.args = {"kernel_size": (5, 5)}
    di.execute()


def dilate_image(image_path, kernel_size):
    img = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    kernel = np.ones(kernel_size, np.uint8)
    # Technically we are "eroding" because our image is expected to be black over white
    return cv.erode(img, kernel, iterations=1)


if __name__ == '__main__':
    main()



