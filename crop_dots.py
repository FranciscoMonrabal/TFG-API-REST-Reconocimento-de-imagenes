import cv2
import os, sys

if __name__ == "__main__":

    samples = os.listdir(r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\dataset\ldots")

    for sample in samples:

        abs_sample = os.path.join(r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\dataset\ldots", sample)
        img = cv2.imread(abs_sample)

        img[0:45, 0:14] = (255, 255, 255)
        img[0:45, 30:45] = (255, 255, 255)

        cv2.imwrite(os.path.join(r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\dataset\ldots_processed", sample), img)

