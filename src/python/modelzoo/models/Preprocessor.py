import numpy as np

from modelzoo.augmentation.Augmenter import Augmenter
from modelzoo.models.Encoder import Encoder
from utils.imageprocessing.Image import Image
from utils.labels.ImgLabel import ImgLabel
from utils.imageprocessing.Backend import resize


class Preprocessor:
    def __init__(self, augmenter: Augmenter, encoder: Encoder, n_classes, img_shape, color_format):
        self.color_format = color_format
        self.img_height, self.img_width = img_shape[:2]
        self.n_classes = n_classes
        self.encoder = encoder
        self.augmenter = augmenter

    def preprocess_train_generator(self, batches: [[(Image, ImgLabel)]]):
        for batch in batches:
            yield self.preprocess_train(batch)

    def preprocess_train(self, dataset: [(Image, ImgLabel)]) -> (np.array, np.array):
        y_batch = []
        x_batch = []
        for img, label, _ in dataset:

            if self.color_format is 'yuv':
                img = img.yuv
            else:
                img = img.bgr

            if self.augmenter is not None:
                img, label = self.augmenter.augment(img, label)

            img, label = resize(img, (self.img_height, self.img_width), label=label)

            x_batch.append(self.encoder.encode_img(img))
            y_batch.append(self.encoder.encode_label(label))

        y_batch = np.concatenate(y_batch, 0)
        x_batch = np.concatenate(x_batch, 0)
        y_batch = np.reshape(y_batch, (len(dataset), -1, self.n_classes + 4))
        x_batch = np.reshape(x_batch, (len(dataset), self.img_height, self.img_width, 3))
        return x_batch, y_batch

    def preprocess(self, img: Image):
        if self.color_format is 'yuv':
            img = img.yuv
        else:
            img = img.bgr
        img = resize(img, (self.img_height, self.img_width))
        return self.encoder.encode_img(img)

    def preprocess_batch(self, batch: [Image]):
        x_batch = np.zeros((len(batch), self.img_height, self.img_width, 3))
        for i, img in enumerate(batch):
            x_batch[i] = self.preprocess(img)
        return x_batch