from flask import Flask, request, jsonify 
import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications import VGG19

from flask_cors import CORS 

app = Flask(__name__)
CORS(app) 
subtypes_psoriasis = ['Guttate Psoriasis', 'Plaque Psoriasis', 'Nail Psoriasis']
disease_type = ['Psoriasis', 'Healthy']

base_path = os.path.dirname(os.path.abspath(__file__))
main_model_path = os.path.join(base_path, 'psoriasis_or_healthy.h5')
subtype_model_path = os.path.join(base_path, 'psoriasis_subtypes.h5')
main_model = load_model(main_model_path)
subtype_model = load_model(subtype_model_path)

vgg_model = VGG19(weights='imagenet', include_top=False, input_shape=(180, 180, 3))
for layer in vgg_model.layers:
    layer.trainable = False

def preprocess_image(img):
    img = cv2.resize(img, (180, 180))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def predict_skin_disease(img):
    
    img = preprocess_image(img)
    img = vgg_model.predict(img)
    img = img.reshape(1, -1)

    pred = main_model.predict(img)[0]
    predicted_class_index = np.argmax(pred)
    predicted_class_name = disease_type[predicted_class_index]
    
    if predicted_class_name == 'Psoriasis':
        print('It is a Psoriasis')
        subtype_pred = subtype_model.predict(img)[0]
        predicted_subtype_index = np.argmax(subtype_pred)
        predicted_class_name = subtypes_psoriasis[predicted_subtype_index]

    print('It is Healthy')
    return predicted_class_name


@app.route('/', methods=['GET'])
def hello_word():
    return "Group 39 Minor"

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image found in the request'}), 400

    imagefile = request.files['image']
    img = cv2.imdecode(np.frombuffer(imagefile.read(), np.uint8), cv2.IMREAD_COLOR)

    predicted_class_name = predict_skin_disease(img)

    return jsonify({'prediction': predicted_class_name})


if __name__ == '__main__':
    app.run(port=8000, debug=True, host='0.0.0.0')