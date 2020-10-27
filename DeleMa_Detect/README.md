- [DeleMa Detect Documentation](#delema-detect-documentation)
  - [Overview](#overview)
    - [```app.py```](#apppy)
    - [```DataVisualization```](#datavisualization)
    - [```Models_notebooks```](#models_notebooks)
    - [```Procfile```](#procfile)
    - [```requirements.txt```](#requirementstxt)
  - [Using the Web App](#using-the-web-app)
    - [On Desktop](#on-desktop)
    - [On Mobile](#on-mobile)
  - [Running DeleMa Detect Locally](#running-delema-detect-locally)
  - [Sample Blood Smear Images](#sample-blood-smear-images)
  - [Contact Us](#contact-us)

# DeleMa Detect Documentation

<img src="https://2020.igem.org/wiki/images/e/e9/T--IISER-Pune-India--delema-demo-desktop-small.gif" alt="DeleMa Detect Demo" width="90%" style="display:block;margin:auto;">

<br>

DeleMa Detect is a Web Application built on a lightweight Python backend that is able to **classify *Plasmodium falciparum* infected blood smear images**. The classification has be documented to be about **~96% accurate** with a **0.96  F1 score** . Results for a blood smear image can be obtained within seconds whereas a traditional approach of testing in laboratory with the requirement of technicians would require atleast a day for accurate results. To classify each image, a Deep Learning convolutional neural network  based Mobilenet_v2 architecture was trained on a set of 27,558 images using open-source software Python, Tensorflow and Keras. 

The final Web App has been deployed on [Heroku](https://delema-detect-igem-iiserpune.herokuapp.com/) for testing and viewing. This repository contains all the files used to build, test and deploy the model. 
You can find more information on how the software was built on our [Software](https://2020.igem.org/Team:IISER-Pune-India/Software) page. 

## Overview 

 <figure>
  <img src=./Deployed-model-screenshots/delema_detect_summary.png width=600>
  <figcaption>Fig.1 - Overview of how DeLeMa Detect was built</figcaption>
</figure> 

### ```app.py```

The main python script uses the Flask micro web framework to create a local host where the model is deployed. It contains auxiliary functions ```model_predict()```, ```index()``` and ```upload()```

1. ```model_predict``` calls the `model.h5` file stored in ```./model/```. We created many models and tested each one's accuracy, size and processing power. Since the size of a few models were greater than 50MB (a soft limit setup by Github) we have uploaded them on [Google Drive](https://drive.google.com/drive/folders/11ULc4FWlB3VScfZIR4y3o8KJgljHZPFe?usp=sharing). Based on the model one wants, it can be downloaded and placed in ```./model/``` 

Although the dimensions of the uploaded image can be anything, each model takes a particular input image size which is controlled and preprocessed in ```app.py```, namely : 
| Sr no | Model | ```target_size``` | 
| ----- | ----- | ----------------- | 
| 1 | MobileNet_v2 | (160, 160) |
| 2 | VGG16 | (100, 100)| 
| 3 | ResNet 50 | (100, 100) | 
| 4 | Custom CNN | (64, 64) | 

This preprocessing of images is done by ```model_predict``` but care should be taken about setting the variable ```target_size``` since each model assumes a different input image size. 



2. ```index()```

This is a Flask function that renders the HTML page written in Jinja 2.0 format stored at ```./static/```

3. ```upload()```

This is another Flask function that enables the user to upload blood smear images from their phone/laptop. The uploaded images are then stored in ```./uploads``` and used for processing and then deleted. A few sample images have already been added to the same folder.


### ```DataVisualization```

This directory contains the Python Notebooks and results of Exploring the Dataset<sup>[1]</sup>. We found the dataset to be very noisy and also came across few misclassified images. 


### ```Models_notebooks``` 

This directory contains all the Python Notebooks that were run on Google Colab to build simple **Machine Learning Classification** models and our **Deep Learning Model**. We employed the technique of **Transfer Learning** and used the networks of : 
1. Mobilenet_v2
2. ResNet50
3. VGG16
4. A Custom-built Convolutional Neural Network 

to train the model. We have also uploaded the performance metrics and plots here for future reference. 

### ```Procfile```

This file is used for deploying as a web application on Heroku. We call the ``app`` method of the ```gunicorn``` module for deploying. 

### ```requirements.txt```

This file contains all the required python (>3.2) modules required for locally running DeleMa-Detect. 

## Using the Web App 

### On Desktop

Open the Heroku Web App hosted at [delema-detect-igem-iiserpune](https://delema-detect-igem-iiserpune.herokuapp.com/). Some sample blood smear images can be found on our [Software page](https://2020.igem.org/Team:IISER-Pune-India/Software) or in the `./uploads/` directory.

 <figure>
  <img src=./Deployed-model-screenshots/desktop-page.png alt="Upload" width="60%" style="display:block;margin:auto;">
  <figcaption>Open our Heroku app and Upload a Blood Smear image </figcaption>
</figure>

<br><br>
The entire Web application has been developed and deployed on Heroku. On visiting the webpage, you will we welcomed by a screen as follows. Now, when a Healthcare worker uses our app, they will click on the `Upload` button to upload a blood smear image. The first image might take ~2-3 seconds to process since the app needs to boot-up. Afterwards, each upload and processing of results takes <1s.

<br><br>



 <figure>
  <img src=./Deployed-model-screenshots/desktop-page-predict.png alt="Predict" width="60%" style="display:block;margin:auto;">
  <figcaption>Click on Predict to get Results and the Probability </figcaption>
</figure>

 <br><br>

On clicking the `Predict` Button, the Image is sent to the Model. The Model Preprocesses the image and generates the outcome in the form of probability scores. These Probability scores and the likelihood of being uninfected is reported. 

<br><br>


<figure>
  <img src=./Deployed-model-screenshots/desktop-page-result-clean.png alt="Clean" width="70%" style="display:block;margin:auto;">
  <figcaption>Results for a Clean or Uninfected Blood Smear Image </figcaption>
</figure>

<br><br>


<figure>
  <img src=./Deployed-model-screenshots/desktop-page-result-infected.png alt="Infected" width="60%" style="display:block;margin:auto;">
  <figcaption>Results for a Parasitized/Infected Blood Smear Image</figcaption>
</figure>
<br><br>

### On Mobile

The [Web App](https://delema-detect-igem-iiserpune.herokuapp.com/) works on mobile too. The procedure is the same. Upload the image and tap on Predict.

<img src="https://2020.igem.org/wiki/images/2/24/T--IISER-Pune-India--delema-demo-mobile-small.gif" alt="DeleMa Detect Demo" width="70%" style="display:block;margin:auto;">


<br>

---

<br>

## Running DeleMa Detect Locally 

1. Clone this Github repository using 
```git clone https://github.com/igemsoftware2020/IISER-Pune-India```

2. Create a Python (>=3.2) virtual environemnt and call it 'delema_detect'.

- Linux: ```python3 -m venv delema_detect```
- Windows: ```python -m venv delema_detect```

A new directory called `delema_detect` will be created. 

Activate the Virtual Environment by running the following.

- Linux: ```source delema_detect/bin/activate```
- Windows: ```.\delema_detect\Scripts\activate```


3. In the new virtual environemnt , run ```pip3 install -r requirements.txt``` to install all dependencies. On Windows, `pip3` will be replaced by `pip`.

4. Download a desired model (VGG16 , Mobilenet_V2 etc) form the [Google Drive link](https://drive.google.com/drive/folders/11ULc4FWlB3VScfZIR4y3o8KJgljHZPFe?usp=sharing) provided and store it in ```./model/```. Based on the model, setup the variable ```target_size``` in ```app.py```

5. Do ```flask run``` or ```python3 app.py``` on the command line and the web app would start running on `localhost:5000` by default.

<br><br>

## Sample Blood Smear Images

We have added upto 20 blood smear images for testing purposes at ```./uploads/```. There are two directories called ```Parasitized``` and ```Uninfected```, each containing upto 10 images. These can be downloaded and tested by running the application locally or on our Heroku platform. 

---

## Contact Us

For clarifications and queries -- Mail [iGEM-IISER-Pune](mailto:igem@sac.iiserpune.ac.in?subject=[igem20_github])@2020
