import argparse

import numpy as np

from train import train
from utils.imageprocessing.BarrelDistortion import BarrelDistortion
from utils.imageprocessing.transform.RandomBlur import RandomBlur
from utils.imageprocessing.transform.RandomChromatic import RandomChromatic
from utils.imageprocessing.transform.RandomEnsemble import RandomEnsemble
from utils.imageprocessing.transform.RandomExposure import RandomExposure
from utils.imageprocessing.transform.RandomHSV import RandomHSV
from utils.imageprocessing.transform.RandomMotionBlur import RandomMotionBlur
from utils.imageprocessing.transform.TransformDistort import TransformDistort

if __name__ == '__main__':
    start_idx = 0
    n_repetitions = 5
    img_res = 416, 416

    parser = argparse.ArgumentParser()
    parser.add_argument("--start_idx", default=start_idx, type=int)
    parser.add_argument("--n_reps", default=n_repetitions, type=int)

    args = parser.parse_args()

    start_idx = args.start_idx
    n_repetitions = args.n_reps
    anchors = np.array([
        [[81, 82],
         [135, 169],
         [344, 319]],
        [[10, 14],
         [23, 27],
         [37, 58]],
    ])
    architecture = [
        {'name': 'conv_leaky', 'kernel_size': (3, 3), 'filters': 16, 'strides': (1, 1), 'alpha': 0.1},
        {'name': 'max_pool', 'size': (2, 2)},
        {'name': 'conv_leaky', 'kernel_size': (3, 3), 'filters': 64, 'strides': (1, 1), 'alpha': 0.1},
        {'name': 'max_pool', 'size': (2, 2)},
        {'name': 'conv_leaky', 'kernel_size': (3, 3), 'filters': 128, 'strides': (1, 1), 'alpha': 0.1},
        {'name': 'max_pool', 'size': (2, 2)},
        {'name': 'conv_leaky', 'kernel_size': (3, 3), 'filters': 256, 'strides': (1, 1), 'alpha': 0.1},
        {'name': 'max_pool', 'size': (2, 2)},
        {'name': 'conv_leaky', 'kernel_size': (3, 3), 'filters': 512, 'strides': (1, 1), 'alpha': 0.1},
        {'name': 'max_pool', 'size': (2, 2)},
        {'name': 'conv_leaky', 'kernel_size': (3, 3), 'filters': 1024, 'strides': (1, 1), 'alpha': 0.1},
        {'name': 'conv_leaky', 'kernel_size': (1, 1), 'filters': 256, 'strides': (1, 1), 'alpha': 0.1},
        {'name': 'conv_leaky', 'kernel_size': (3, 3), 'filters': 512, 'strides': (1, 1), 'alpha': 0.1},
        {'name': 'predict'},
        {'name': 'route', 'index': [-4]},
        {'name': 'conv_leaky', 'kernel_size': (1, 1), 'filters': 128, 'strides': (1, 1), 'alpha': 0.1},
        {'name': 'upsample', 'size': 2},
        {'name': 'route', 'index': [-1, 8]},
        {'name': 'conv_leaky', 'kernel_size': (3, 3), 'filters': 256, 'strides': (1, 1), 'alpha': 0.1},
        {'name': 'predict'}
    ]

    model_name = 'yolov3_pp{}x{}'.format(img_res[0], img_res[1])

    augmenter = RandomEnsemble([
        (0.2, TransformDistort(BarrelDistortion((416, 416), rad_dist_params=[0.7, 0], tangential_dist_params=[0.7, 0]),
                               2.0)),
        (1.0, RandomExposure((0.8, 1.2))),
        (0.2, RandomMotionBlur(1.0, 2.0, 15)),
        (0.2, RandomBlur((5, 5))),
        (1.0, RandomHSV((.9, 1.1), (0.8, 1.2), (0.8, 1.2))),
        (1.0, RandomChromatic((-2, 2), (0.99, 1.01), (-2, 2))),
    ])

    image_source = ['resource/ext/samples/daylight_course1',
                    'resource/ext/samples/daylight_course5',
                    'resource/ext/samples/daylight_course3',
                    'resource/ext/samples/iros2018_course1',
                    'resource/ext/samples/iros2018_course5',
                    'resource/ext/samples/iros2018_flights',
                    'resource/ext/samples/basement_course3',
                    'resource/ext/samples/basement_course1',
                    'resource/ext/samples/iros2018_course3_test',
                    'resource/ext/samples/various_environments',
                    'resource/ext/samples/real_bg'
                    ]

    for i in range(start_idx, start_idx + n_repetitions):
        train(architecture=architecture,
              work_dir='thesis/datagen/{0:s}_i{1:02d}'.format(model_name, i),
              img_res=img_res,
              augmenter=augmenter,
              image_source=image_source,
              anchors=anchors,
              epochs=50,
              batch_size=16,
              n_samples=20000,
              min_obj_size=0.01,
              max_obj_size=2.0,
              min_aspect_ratio=0.3,
              max_aspect_ratio=4.0,
              initial_epoch=0,
              color_format='bgr')