import cv2
import os

if __name__ == "__main__":


    show_first = True

    folders = os.listdir(r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\dataset")
    for folder in folders:
       samples = os.listdir(os.path.join(r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\dataset", folder))
       folder_exits = False
       for sample in samples:
           abs_sample = os.path.join(r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\dataset", folder, sample)
           print(abs_sample)
           img = cv2.imread(abs_sample, cv2.IMREAD_GRAYSCALE)

           if show_first:
               cv2.imshow("color", img)

           if not folder_exits:
               os.mkdir(os.path.join(r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\dataset_gray", folder))
               folder_exits = True

           cv2.imwrite(os.path.join(r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\dataset_gray", folder, sample), img)
