import os
import sys
import timeit

import numpy as np

from imggen.DetermImgGen import DetermImgGen
from imggen.RandomImgGen import RandomImgGen

PROJECT_ROOT = '/home/phil/Desktop/thesis/code/dronevision'

WORK_DIRS = [PROJECT_ROOT + '/samplegen/src/python',
             PROJECT_ROOT + '/droneutils/src/python',
             PROJECT_ROOT + '/dvlab/src/python']
for work_dir in WORK_DIRS:
    sys.path.insert(0, work_dir)
os.chdir(PROJECT_ROOT)

from fileaccess.SetFileParser import SetFileParser
from timing import tic, toc, tuc
from shotgen.ShotLoad import ShotLoad

background_path = ["samplegen/resource/backgrounds/lmsun/",
                   "samplegen/resource/backgrounds/google-fence-gate-industry/"]
#background_path = "samplegen/resource/backgrounds/single"
#background_path = "samplegen/resource/backgrounds/single/"
# sample_path = "resource/samples/single_background_test/"
sample_path = "resource/samples/mult_gate_train/"
shot_path = "samplegen/resource/shots/mult_gate_train/"

n_backgrounds = 50000
batch_size = 1000
n_batches = int(np.ceil(n_backgrounds / batch_size))

if not os.path.exists(sample_path):
    os.makedirs(sample_path)
tic()

setwriter = SetFileParser(sample_path, img_format='jpg', label_format='pkl')

for i in range(n_batches):
    tic()
    shots, shot_labels = ShotLoad(shot_path, img_format='bmp').get_shots(n_shots=250)
    samples, labels = RandomImgGen(background_path, out_format='yuv').generate(
        shots, shot_labels,
        n_backgrounds=batch_size)

    setwriter.write(samples, labels)
    toc("Batch: {1:d}/{2:d} - {0:d}/{3:d} samples generated ".format(
        int(len(samples) * (i + 1)), i, n_batches, int(n_batches * batch_size)))
    tuc("Total time: ")

toc("Finished. Total run time ")