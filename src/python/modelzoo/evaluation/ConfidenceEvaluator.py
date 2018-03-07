import numpy as np

from modelzoo.evaluation.DetectionEvaluator import DetectionEvaluator
from modelzoo.evaluation.Metric import Metric
from modelzoo.models.Predictor import Predictor
from utils.BoundingBox import BoundingBox
from utils.fileaccess.utils import load_file, save_file
from utils.imageprocessing.Backend import imread
from utils.labels.ImgLabel import ImgLabel
from utils.timing import tic, toc


class ConfidenceEvaluator(DetectionEvaluator):
    def __init__(self, model: Predictor, metrics: [Metric], confidence_levels=11, out_file=None, verbose=True,
                 color_format='bgr'):
        super().__init__(metrics=metrics, out_file=out_file, verbose=verbose, color_format=color_format)
        self.model = model
        self.confidence_levels = np.round(np.linspace(1.0, 0, confidence_levels), 2)

    def evaluate_sample(self, label_pred: ImgLabel, label_true: ImgLabel, img=None):

        boxes_predicted = BoundingBox.from_label(label_pred)
        results_by_conf = {}
        labels_pred = {}
        for c in self.confidence_levels:
            label_reduced = BoundingBox.to_label(self.model.postprocessor.filter(boxes_predicted, c))
            results_by_m_c = {}
            for name, m in self.metrics.items():
                m.update(label_true=label_true, label_pred=label_reduced)
                results_by_m_c[name] = m.result
                if m.show:
                    m.show_result(img)

            results_by_conf[c] = results_by_m_c
            labels_pred[c] = label_reduced

        # resort so we have for each metric a dict with results for each confidence
        results_by_m = {}
        for name in self.metrics.keys():
            results_by_m[name] = {c: results_by_conf[c][name] for c in self.confidence_levels}

        return results_by_m, labels_pred

    def evaluate(self, result_file: str):
        results = {m: [] for m in self.metrics.keys()}
        file_content = load_file(result_file)
        labels_true = file_content['labels_true']
        labels_raw = file_content['labels_pred']
        image_files = file_content['image_files']
        tic()
        labels_pred = []
        for i in range(len(labels_true)):
            image = imread(image_files[i], self.color_format)
            sample_result, label_pred = self.evaluate_sample(labels_raw[i], labels_true[i], image)
            labels_pred.append(label_pred)

            for m in self.metrics.keys():
                results[m].append(sample_result[m])

        if self.verbose:
            toc("Evaluated file in ")

        if self.out_file is not None:
            content = {'results': results,
                       'labels_true': labels_true,
                       'labels_pred': labels_pred}
            save_file(content, self.out_file)

        return results