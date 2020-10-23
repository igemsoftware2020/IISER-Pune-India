from __future__ import division, print_function
# coding = utf8
import sys
import os
import glob
import re
import numpy as np

# Keras utils
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, render_template, url_for, request, redirect 
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras.save()
MODEL_PATH='./model/VGG_94.52_11102020_8 49.h5'
model = load_model(MODEL_PATH)
probability = 0.3

def model_predict(img_path,model_path):
	
    img = image.load_img(img_path,target_size=(100,100))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array,axis=0) # changes input shape to a tensor (1,160,160,3)
    #img_array = preprocess_input(img_array) # preprocess input based on mobilenet_v2 conventions

    output = model.predict(img_array).flatten()
    prediction = output[0]
    
    return prediction

@app.route('/', methods=['GET'])
def index():
    # displays main page
    return render_template('index.html')
	
@app.route('/predict',methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        prediction = model_predict(file_path, MODEL_PATH)

        # Process your result for human
        # Preserve the 0- and 1- prefixes
        if prediction <= probability:
            result = f"1-The Image looks Parasitized.\nThe probability that the blood smear is uninfected is {prediction:.3} "
        else:
            result=f"0-The Image looks Uninfected.\nThe probability that the blood smear is uninfected is {prediction:.3} "
        
        return result
    return None
	

if __name__ == '__main__':
    app.run(debug=True)
