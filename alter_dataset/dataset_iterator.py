import cv2
import os


class DatasetIterator:

    def __init__(self, ds_path, ds_path_dest, func, overwrite, **kwargs):
        self.dataset_path = ds_path
        self.dataset_path_destination = ds_path_dest
        self.function = func
        self.overwrite = overwrite
        self.args = kwargs

    def execute(self):

        folders = os.listdir(self.dataset_path)
        for folder in folders:
            samples = os.listdir(os.path.join(self.dataset_path, folder))

            for sample in samples:
                if not os.path.isdir(os.path.join(self.dataset_path_destination, folder)):
                    os.mkdir(os.path.join(self.dataset_path_destination, folder))

                abs_sample = os.path.join(self.dataset_path, folder, sample)
                print(abs_sample)
                img = self.function(abs_sample, **self.args)

                ds_path_img = self._calculate_img_sufix_name(
                    os.path.join(self.dataset_path_destination, folder, sample))
                cv2.imwrite(ds_path_img, img)

    def _calculate_img_sufix_name(self, img_name):

        ret = img_name

        if not self.overwrite and os.path.isfile(img_name):
            sufix = ""
            i = img_name.index(".j")
            while os.path.isfile(ret):
                sufix += "x"
                ret = img_name[:i] + sufix + img_name[i:]

        return ret
