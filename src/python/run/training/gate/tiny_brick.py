import pprint as pp

from modelzoo.backend.tensor.Training import Training
from modelzoo.backend.tensor.callbacks.TestMetrics import TestMetric
from modelzoo.backend.tensor.yolo.AveragePrecisionYolo import AveragePrecisionYolo
from modelzoo.evaluation.ConfidenceEvaluator import ConfidenceEvaluator
from modelzoo.evaluation.MetricDetection import MetricDetection
from modelzoo.evaluation.ModelEvaluator import ModelEvaluator
from modelzoo.models.yolo.Yolo import Yolo
from utils.fileaccess.GateGenerator import GateGenerator
from utils.fileaccess.utils import create_dirs, save_file
from utils.imageprocessing.transform.MavvAugmenter import MavvAugmenter
from utils.imageprocessing.transform.RandomBrightness import RandomBrightness
from utils.imageprocessing.transform.RandomEnsemble import RandomEnsemble
from utils.imageprocessing.transform.RandomShift import RandomShift
from utils.imageprocessing.transform.TransformFlip import TransformFlip
from utils.workdir import cd_work
import numpy as np

cd_work()

batch_size = 4

image_source = ["resource/ext/samples/brick_room/"]
test_image_source = ['resource/ext/samples/brick_room_test/']
max_epochs = 200

predictor = Yolo.tiny_yolo(class_names=['gate'], batch_size=batch_size,
                           color_format='bgr')
data_generator = GateGenerator(image_source, batch_size=batch_size, valid_frac=0.1,
                               color_format='bgr', label_format='xml')
test_gen = GateGenerator(test_image_source, batch_size=batch_size, valid_frac=0, color_format='bgr', label_format='xml')

augmenter = RandomEnsemble([(1.0, RandomBrightness(0.5, 2.0)),
                            (0.5, TransformFlip()),
                            (0.2, RandomShift(-.3, .3))])

model_name = predictor.net.__class__.__name__

name = 'tiny_airsim'
result_path = 'logs/' + name + '/'
test_result = result_path + 'results/industrial_room-'

create_dirs([result_path])

predictor.preprocessor.augmenter = augmenter

params = {'optimizer': 'adam',
          'lr': 0.001,
          'beta_1': 0.9,
          'beta_2': 0.999,
          'epsilon': 1e-08,
          'decay': 0.0005}

predictor.compile(params=params)

test_metric = TestMetric(test_gen,
                         ModelEvaluator(predictor, verbose=False),
                         ConfidenceEvaluator(predictor, metrics=[MetricDetection(show_=False)], out_file=test_result,
                                             color_format='bgr'))
training = Training(predictor, data_generator,
                    out_file=model_name + '.h5',
                    patience_early_stop=-1,
                    patience_lr_reduce=10,
                    log_dir=result_path,
                    stop_on_nan=True,
                    initial_epoch=0,
                    epochs=max_epochs,
                    log_csv=True,
                    lr_reduce=0.1,
                    callbacks=[test_metric])

create_dirs([result_path, result_path + '/results/'])

pp.pprint(training.summary)

save_file(training.summary, 'training_params.txt', result_path, verbose=False)

training.fit_generator()