import copy

from utils.imageprocessing.Backend import crop, resize
from utils.imageprocessing.DistortionModel import DistortionModel
from utils.imageprocessing.Image import Image
from utils.imageprocessing.transform.ImgTransform import ImgTransform
from utils.labels.ImgLabel import ImgLabel


class TransformDistort(ImgTransform):
    def __init__(self, dist_model: DistortionModel, crop=0.2):
        self.crop = crop
        self.dist_model = dist_model

    def transform(self, img: Image, label: ImgLabel):
        img_aug = img.copy()
        label_aug = copy.deepcopy(label)
        h, w = img.shape[:2]
        h_crop = int(self.crop * h)
        w_crop = int(self.crop * w)
        img_aug, label_aug = self.dist_model.distort(img_aug, label_aug)

        img_aug, label_aug = crop(img_aug, (w_crop, h_crop), (w - w_crop, h - h_crop), label_aug)

        img_aug, label_aug = resize(img_aug, (h, w), label=label_aug)

        return img_aug, label_aug