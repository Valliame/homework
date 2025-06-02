import os
import numpy as np

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from keras.models import load_model
from tensorflow.keras.preprocessing import image

model = load_model("./data/model.h5")

img_path = "./data/cat.png/"
img = image.load_img(img_path, target_size = (224,224))
img_array = image.img_to_array(img)
print(img_array.shape)

img_batch = np.expand_dims(img_array, axis=0)
print(img_batch.shape)

from tensorflow.keras.applications.mobilenet import preprocess_input

img_processed = preprocess_input(img_batch)

prediction = model.predict(imp_processed)
print(prediction)