from modelzoo.evaluation.evalset import evalset
from utils.labels.ObjectLabel import ObjectLabel
from utils.workdir import cd_work

cd_work()

# models = [name for name in os.listdir('out/0108/')]
models = [
    # 'yolov3_gate_realbg416x416',
    # 'yolov3_gate_uniform416x416',
    # 'yolov3_gate_dronemodel416x416',
    # 'yolov3_gate_varioussim416x416',
    # 'yolov3_gate_mixed416x416',
    # 'yolov3_allgen416x416',
    # 'yolov3_hsv416x416',
    # 'yolov3_blur416x416',
    # 'yolov3_chromatic416x416',
    # 'yolov3_exposure416x416',
    # 'yolov3_40k416x416',
    # 'yolov3_allview416x416',
    # 'yolov3_gate416x416',
    # 'yolov3_arch2416x416',
    'yolov3_arch_random416x416',
    # 'yolov3_arch_race416x416',

]
dataset = 'iros2018_course_final_simple_17gates'


work_dir = 'out/thesis/datagen/'
n_iterations = 2
ObjectLabel.classes = ['gate']
exp_name = 'datagen'
for model in models:
    for i in range(0, n_iterations):
        model_folder = model + '_i0{}'.format(i)
        prediction_file = 'predictions'.format(dataset)
        try:
            evalset(name=exp_name,
                    result_path=work_dir + model_folder + '/test_' + dataset + '/',
                    result_file=prediction_file,
                    batch_size=4,
                    model_src=work_dir + model_folder,
                    preprocessing=None,
                    color_format='bgr',
                    image_source=['resource/ext/samples/{}/'.format(d)])
        except FileNotFoundError:
            print("Not found: {}".format(model_folder))