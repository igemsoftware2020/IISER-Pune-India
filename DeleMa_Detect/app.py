from __future__ import division, print_function
# coding = utf8
import sys
import os
import glob
import re
import numpy as np
import time

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
#MODEL_PATH='./model/custom_cnn_lenet_val_9539_oct_24_1100.h5' 
#MODEL_PATH='./model/VGG_94.52_11102020_8 49.h5'

MODEL_PATH = './model/model.h5'
input_size=(100,100)

model = load_model(MODEL_PATH)
probability = 0.3

def model_predict(img_path,model_path,input_size):
	
    img = image.load_img(img_path,target_size=input_size)
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

        # Append timestamp to ensure unique filename
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename + str(int(time.time()))))
        f.save(file_path)

        # Make prediction
        prediction = model_predict(file_path, MODEL_PATH, input_size)

        # Process your result for human
        # Preserve the 0- and 1- prefixes
        if prediction <= probability:
            result = f"1-The Image looks Parasitized.\nThe probability that the blood smear is uninfected is {prediction:.3} "
        else:
            result=f"0-The Image looks Uninfected.\nThe probability that the blood smear is uninfected is {prediction:.3} "


        # Delete the file
        os.remove(file_path)
                
        return result
    return None
	

if __name__ == '__main__':
    app.run(debug=True)
