from tensorflow.keras.preprocessing import image
import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

TRAIN_DATA_DIR = "./data/train_data/"
VALIDATION_DATA_DIR = "./data/val_data/"
TRAIN_SAMPLES = 500
VALIDATION_SAMPLES = 500
NUM_CLASSES = 2
IMG_WIDTH, IMG_HEIGHT = 224, 224
BATCH_SIZE = 64

from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input

train_datagen = image.ImageDataGenerator(
    preprocessing_function = preprocess_input,
    rotation_range = 20,
    width_shift_range = 0.2,
    height_shift_range = 0.2,
    zoom_range = 0.2
)

val_datagen = image.ImageDataGenerator(preprocessing_function = preprocess_input)

train_generator = train_datagen.flow_from_directory(
    TRAIN_DATA_DIR,
    target_size = (IMG_WIDTH, IMG_HEIGHT),
    batch_size = BATCH_SIZE,
    shuffle = True,
    seed = 12345,
    class_mode="categorical"
)

val_generator = val_datagen.flow_from_directory(
    VALIDATION_DATA_DIR,
    target_size = (IMG_WIDTH, IMG_HEIGHT),
    batch_size = BATCH_SIZE,
    shuffle = True,
    seed = 12345,
    class_mode="categorical"
)

from tensorflow.keras.layers import (
    Input,
    Flatten,
    Dense,
    Dropout,
    GlobalAveragePooling2D
)

from tensorflow.keras.models import Model

def model_maker():
    base_model = MobileNet(include_top = False, input_shape=(IMG_WIDTH, IMG_WEIGHT, 3))
    for layer in base_model.layers[:]:
        layer.trainable = False

        input = Input(shape=(IMG_WIDTH, IMG_WEIGHT, 3))
        custom_model = base_model(input)
        custom_model = GlobalAveragePooling2D()(custom_model)
        custom_model = Dense(64, activation="relu")(custom_model)
        custom_model = Dropout(0.5)(custom_model)
        prediction = Dense(NUM_CLASSES, activation="softmax")(custom_model)
        return Model(inputs = input, outputs = prediction)

from tensorflow.keras.optimizers import Adam

model = model.maker()
model.compile(
    loss = "categorical_crossentropy",
    optimizer=Adam(),
    metrics=["acc"]
)

import math
num_steps = math.cell(float(TRAIN_SAMPLES)/BATCH_SIZE)

model.fit(
    train_generator,
    steps_per_epoch=num_steps,
    epochs=10, # Шаг обучения
    validation_data=val_generator,
    validation_steps=num_steps,
)

print(val_generator.class_indices)

model.save("./data/model.h5")

# img_path = "./data/luna.jpg/"
# img = image.load_img(img_path, target_size = (224,224))

# import as np

# img_array = image.img_to_array(img)
# print(img_array.shape)

# img_batch = np.expand_dims(img_array, axis=0)
# print(img_batch.shape)

# from tensorflow.keras.applications.resnet50 import preprocess_input

# img_processed = preprocess_input(img_batch)

# from tensorflow.keras.applications.resnet50 import ResNet50

# model = ResNet50()
# prediction = model.predict(img_processed)

# from tensorflow.keras.applications.resnet50 import decode_predictions
# print(decode_predictions(prediction, top=5)[0])

# plt.imshow(img)
# plt.show()