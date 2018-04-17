import numpy as np

from modelzoo.models.Decoder import Decoder
from utils.BoundingBox import BoundingBox


class GateNetDecoder(Decoder):
    def __init__(self,
                 norm=(416, 416),
                 grid=(13, 13),
                 n_polygon=4):
        self.n_polygon = n_polygon
        self.grid = grid
        self.norm = norm

    def decode_netout_to_boxes(self, label_t):
        """
        Convert label tensor to objects of type Box.
        :param label_t: y as fed for learning
        :return: boxes
        """
        label_t = np.reshape(label_t, [self.grid[0], self.grid[1], -1, 1 + self.n_polygon])
        coord_t = label_t[:, :, :, :self.n_polygon]
        class_t = label_t[:, :, :, self.n_polygon:]
        coord_t_dec = self.decode_coord(coord_t)
        coord_t_dec = np.reshape(coord_t_dec, (-1, self.n_polygon))
        class_t = np.reshape(class_t, (-1, 1))
        boxes = BoundingBox.from_tensor_centroid(class_t, coord_t_dec)

        return boxes

    def decode_coord(self, coord_t):
        """
        Decode the coordinates of the bounding boxes from the label tensor to absolute coordinates in the image.
        :param coord_t: label tensor (only coordinates)
        :return: label tensor in absolute coordinates
        """
        coord_t_dec = coord_t.copy()
        offset_y, offset_x = np.mgrid[:self.grid[0], :self.grid[1]]

        offset_x = np.expand_dims(offset_x, -1)

        offset_y = np.expand_dims(offset_y, -1)

        coord_t_dec[:, :, :, 0] += offset_x
        coord_t_dec[:, :, :, 1] += offset_y
        coord_t_dec[:, :, :, 0] *= (self.norm[1] / self.grid[1])
        coord_t_dec[:, :, :, 2] *= (self.norm[1] / self.grid[1])
        coord_t_dec[:, :, :, 1] *= (self.norm[0] / self.grid[0])
        coord_t_dec[:, :, :, 3] *= (self.norm[0] / self.grid[0])

        coord_t_dec[:, :, :, 1] = self.norm[0] - coord_t_dec[:, :, :, 1]

        return coord_t_dec

    def decode_netout_to_label(self, label_t):
        """
        Convert label tensor to an object of class ImgLabel
        :param label_t: label-tensor as fed for learning
        :return: label containing objects bounding box and names
        """
        boxes = self.decode_netout_to_boxes(label_t)
        return BoundingBox.to_label(boxes)