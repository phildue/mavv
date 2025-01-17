from evaluation.evaluation import evaluate_labels
from utils.imageprocessing.transform.TransformResize import TransformResize
from utils.labels.ObjectLabel import ObjectLabel
from utils.workdir import cd_work

cd_work()

# models = [name for name in os.listdir('out/0108/')]


models = [
    'mavnet',
    'mavnet_lowres160',
    'mavnet_lowres320',
    'mavnet_strides',
    'mavnet_strides3_pool2',
    'mavnet_strides4_pool1',
    # 'yolov3_width0',
    # 'yolov3_width1',
    # 'yolov3_width2',
    # 'yolov3_width3',
    # 'yolo_lowres160',
]
preprocessing = [
    None,
    [TransformResize((160, 160))],
    [TransformResize((320, 320))],
    [TransformResize((320, 320))],
    [TransformResize((320, 320))],
    [TransformResize((320, 320))],
    # [TransformResize((160, 160))],
    # None,
    # None,
    # None,
    # None,
    # [TransformResize((160, 160))],
]

dataset = 'iros2018_course_final_simple_17gates'

work_dir = 'out/'
n_iterations = 2
ObjectLabel.classes = ['gate']
for i_m, model in enumerate(models):
    for i in range(0, n_iterations):
        model_folder = model + '_i0{}'.format(i)
        label_file = work_dir + model_folder + '/test_' + dataset + '/' + 'predictions.pkl'
        for iou_thresh in [0.4, 0.6, 0.8]:
            try:
                evaluate_labels(name='results_iou{}'.format(iou_thresh),
                                preprocessing=preprocessing[i_m],
                                min_box_area=0.001,
                                max_box_area=2.0,
                                min_aspect_ratio=0.33,
                                max_aspect_ratio=3.0,
                                iou_thresh=iou_thresh,
                                model_src=work_dir + model_folder,
                                label_file=label_file,
                                result_path=work_dir + model_folder + '/test_' + dataset + '/',
                                show=1)
            except FileNotFoundError:
                print("Missing: " + label_file)
                continue
