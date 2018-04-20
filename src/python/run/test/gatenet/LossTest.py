import random

import keras.backend as K

from modelzoo.models.gatenet.GateNet import GateNet
from utils.fileaccess.GateGenerator import GateGenerator
from utils.imageprocessing.Backend import annotate_text
from utils.imageprocessing.Imageprocessing import show, COLOR_GREEN, COLOR_RED
from utils.workdir import cd_work

cd_work()
batch_size = 99
predictor = GateNet.v0(batch_size=batch_size,
                       color_format='bgr')

dataset = GateGenerator(["resource/ext/samples/industrial_new/"], batch_size=batch_size,
                        color_format='bgr', label_format='xml', n_samples=batch_size).generate()
batch = next(dataset)
N = 5
idx = random.randint(0, 99 - N)

# img_enc = ssd.preprocessor.encode_img(img)
labels1_enc = []
labels2_enc = []
for i in range(N):
    label1_t = predictor.encoder.encode_label(batch[i][1])
    label1_t = K.np.expand_dims(label1_t, 0)
    labels1_enc.append(label1_t)
    label2_t = predictor.encoder.encode_label(batch[i + 5][1])
    label2_t = K.np.expand_dims(label2_t, 0)
    labels2_enc.append(label2_t)

labels1_t = K.np.concatenate(labels1_enc, 0)
labels2_t = K.np.concatenate(labels2_enc, 0)
# label_dec = ssd.postprocessor.decode_label(label_enc)
# label_enc_2 = ssd.preprocessor.encode_label(label_2)
sess = K.tf.InteractiveSession()
loss = predictor.loss.compute(y_pred=K.constant(labels2_t, K.tf.float32),
                              y_true=K.constant(labels1_t, K.tf.float32)).eval()
print("Total Loss:", K.np.sum(loss))

for i in range(N):
    img = batch[i][0]
    label_true = batch[i][1]
    label_pred = batch[i + 5][1]
    img = annotate_text(str(loss[i]), img, thickness=2, color=(255, 255, 255))
    show(img, labels=[label_true, label_pred], colors=[COLOR_GREEN, COLOR_RED])