from utils.imageprocessing.Backend import imread
from utils.imageprocessing.Imageprocessing import show
from utils.imageprocessing.transform.TransformChromAbberr import TransformChromAbberr
from utils.workdir import cd_work

cd_work()
example_path = 'doc/thesis/fig/gate_example'
img = imread(example_path + '.jpg', 'bgr')

img_t, _ = TransformChromAbberr(scale=(1, 1.01, 1), t_x=(-0.1, 0, -5.0), t_y=(10, -0, 0.01)).transform(img, )

show(img, name='Original')
show(img_t, 'Chromatic')

# imwrite(img_t, example_path + '_chromatic.jpg')
