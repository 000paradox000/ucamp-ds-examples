import os

import tensorflow as tf
from keras.preprocessing import image
import numpy as np


def main():
    # load model
    model = tf.keras.models.load_model("files/models/model.h5")

    names = [
        'avión',
        'automóvil',
        'ave',
        'gato',
        'ciervo',
        'perro',
        'rana',
        'caballo',
        'barco',
        'camión'
    ]

    for file_name in os.listdir("files/samples"):
        path = os.path.join(f"files/samples/{file_name}")
        img = prepare_image(path)

        prediction = model.predict(img)
        filtered_prediction = filter_prediction(prediction)
        argmax_prediction = np.argmax(prediction, axis=1)

        name = None
        if any(filtered_prediction):
            idx = filtered_prediction.index(1)
            name = names[idx]

        print("-" * 30)
        print(file_name)
        print(f"Prediction: {prediction}")
        print(f"Argmax Prediction: {argmax_prediction}")
        print(f"FilteredPrediction: {filtered_prediction}")
        print(f"Object found: {name}")

def prepare_image(path):
    img = image.image_utils.load_img(path, target_size=(32, 32))
    img = image.image_utils.img_to_array(img)
    img = img.reshape(1, 32, 32, 3)
    img = img.astype('float32')
    img = img / 255.0

    return img


def filter_prediction(prediction):
    return (prediction > 0.5).astype("int32").flatten().tolist()


if __name__ == "__main__":
    main()
