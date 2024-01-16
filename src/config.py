import uuid
import os


class Config:

    _image_name = None

    images_path = r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\images"
    rec_img_ext = r"recieved_imgs"
    sen_img_ext = r"sent_imgs"

    models_path = r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\models"
    model_name = r"symbol_recognition_9"
    dataset_path = r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\datasets"
    dataset_name = r"dataset"

    def get_dataset_path(self):
        return os.path.join(self.dataset_path, self.dataset_name)

    def get_model_path(self):
        return os.path.join(self.models_path, self.model_name)

    def get_image_path(self):
        return os.path.join(self.images_path, self.rec_img_ext, self._image_name)

    def get_final_image_path(self):
        return os.path.join(self.images_path, self.sen_img_ext, self._image_name)

    def generate_img_name(self):
        if self._image_name is None:
            self._image_name = f"{uuid.uuid4()}.jpeg"

        return self._image_name

    def __init__(self):
        self.generate_img_name()
