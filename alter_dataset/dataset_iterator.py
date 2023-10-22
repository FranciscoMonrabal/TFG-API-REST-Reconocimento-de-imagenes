import cv2
import os


class DatasetIterator:

    def __init__(self, ds_path, ds_path_dest, func):
        self.dataset_path = ds_path
        self.dataset_path_destination = ds_path_dest
        self.function = func

    def execute(self):

        folders = os.listdir(self.dataset_path)
        for folder in folders:
            samples = os.listdir(os.path.join(self.dataset_path, folder))
            folder_exits = False

            for sample in samples:
                if not folder_exits:
                    os.mkdir(os.path.join(self.dataset_path_destination, folder))
                    folder_exits = True

                abs_sample = os.path.join(self.dataset_path, folder, sample)
                print(abs_sample)
                img = self.function(abs_sample)
                cv2.imwrite(os.path.join(self.dataset_path_destination, folder, sample), img)



