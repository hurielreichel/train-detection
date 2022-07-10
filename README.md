# train-detection
Detection of trains in SWISSIMAGE for Analysis of High Resolution Imagery Class (WWU)

## Introduction

In a world where the climate crisis is becoming increasingly pressing, societies need to transition to greener modes of transportation. In particular, public transport provides an important opportunity to reduce traffic emissions. In Switzerland, an index of public transport quality is available and we aim to compare CNN detections on aerial imagery to this index. We do this in a way that allows reproducibility and a notion of public transport quality can be computed in other places. 

### Data

Through the [swisstopo open data portal](map.geoadmin.ch), one can have access to high resolution RGB imagery all over Switzerland from 2018 until recently. These images are called [SWISSIMAGE](https://www.swisstopo.admin.ch/de/geodata/images/ortho/swissimage10.html) and can be acquired with 10 cm resolution in either .tif format or through a WMS. 

Although, in order to detect trains, we need labels. In this case, our base dataset is a combination of self-made labels, and others made by colleagues. This vector file can be found [here](trains-data/vehicles-labels.geojson). The image below gives an idea of this dataset plot over the SWISSIMAGE from 2018. 

![Labels for trains over SWISSIMAGE 2018](fig/labels.png)

## The Model

For this task we developed a Faster Recurrent-Convolutional Neural Network (Faster R-CNN) using ResNet as backbone model. Our code was mainly based in [Rawat's implementation for Airplanes detection](https://github.com/ShubhankarRawat/Airplane-Detection-for-Satellites) with some hyperparameter tuning for our case, including a whole lot of data preparation. All these scripts can be found [here](src/) too. 

If you wish to check our hyperparameters in more details, we invite you to check mainly [this file](src/keras_frcnn/config.py), and also [this one](src/keras_frcnn/resnet.py), where you shall understand the implement architecture as well. We can say in advance that we don't go far from the classic proposition, as, e.g., the one proposed by [Xu](https://towardsdatascience.com/faster-r-cnn-object-detection-implemented-by-keras-for-custom-data-from-googles-open-images-125f62b9141a). 

## Comparison to Public Transport Quality Data

As mentioned, the goal was to compare this dataset to the [Public Transport Connection Quality ARE from swisstopo](https://www.are.admin.ch/verkehrserschliessung). For that reason, we applied a simple spatial query comparing these polygons to the locations of the detected trains in a buffer area of 100 m around [swiss railways](https://www.bav.admin.ch/bav/de/home/verkehrstraeger/eisenbahn.html). This is done with [wms-extractor code](src/wms-extractor.py), which also clips the WMS from swisstopo in 100 m images for predictions. Something similar is done with the input images (downloaded from [here](https://www.swisstopo.admin.ch/en/geodata/images/ortho/swissimage10.html#musterdaten) with [this code](src/Files.py).

The detections are delivered in two ways : first, every prediction image is overploted by the predicted bounding boxes and labels. Second, a [csv](bounding_box_coordinates_ans.csv) with the bounding box pixel coordinates are given together with every image filename. A script to extract these coordinates to their centroid into a [geojson file](trains-data/detected-centroids.geojson) is available [here](src/extract-centroids.R).   

## Hardware
 
We ran our model and its tests in the HPC from the University of Münster [PALMA](https://www.uni-muenster.de/CoCoS/Systeme/PALMA.html) using the GeForce RTX 2080, and mainly GeForce RTX Titan. Local tests were made with NVIDIA Quadro RTX as well.

## Results

![Example of detection in SWISSIMAGE](fig/example.png)

We obtained a classifier accuracy for bounding boxes from RPN of 97.6 %. The loss and mAP curves were implemented for validation purposes :

![Loss Curve with 130 epochs](fig/loss_function.png)

The mAP can also be observed below :

![Loss Curve with 130 epochs](fig/mAP.png)

plot of quality vs. centroids

correlation plot

## Usage

First of all, it's important to mention that we're in an older version of tensorflow (1.15.0) and keras (2.0.3), so be careful with the installation, described in the following. The python version we used was 3.7.13 and we recommend it due to tensorflow and keras compatibility. You can create an environment in conda, e.g., the following way:

```
$ conda create -n <envname> python=3.7.13
```

In the following we installed tensorflow-gpu, which automatically install all you need coming from tensorflow. If you're not using GPU, try tensforflow==1.15.0, but be careful, it will take long and some troubleshooting with conda may still be necessary. We then installed keras, another group of packages and this is it. 
 
```
$ conda install tensorflow-gpu==1.1.5.0
$ pip install keras==2.0.3
$ pip install h5py==2.10.0
$ pip install opencv-python==4.6.0.66
$ pip install matplotlib==3.5.2
# pip install pandas==1.3.5
``` 

You can also try $ pip install -r requirements.txt , but we do not recommend so, as the order of installation was quite important to make this environment properly work. 

Once the the environment is ready, you can just make sure everything is in its place. Our training images were in a directory called training_images. If you're using our annotation file, and exectung exactly as we did, then you can simply run:

```
$ python src/train_frcnn.py -o simple -p src/annotation.txt --input_weight_path weights/resnet50_weights_tf_dim_ordering_tf_kernels.h5 --num_epochs 130
```

Once you trained the model, you may find the mAP and loss related files. It's important then to run the following command to create a folder where the prediction will be made on. 

```
$ mkdir results_imgs
```

Our prediction images were in a directory called tst-img, therefore, we ran the given command to make predictions :

```
$ python src/test_frcnn -p tst-img/
```

Then you should have the images and the final csv with results. 

## References

[Faster R-CNN Explained](https://medium.com/@smallfishbigsea/faster-r-cnn-explained-864d4fb7e3f8)

[Faster R-CNN (object detection) implemented by Keras for custom data from Google’s Open Images Dataset V4](https://towardsdatascience.com/faster-r-cnn-object-detection-implemented-by-keras-for-custom-data-from-googles-open-images-125f62b9141a)

[Airplanes Detection for Satellite using Faster RCNN] (https://towardsdatascience.com/airplanes-detection-for-satellite-using-faster-rcnn-d307d58353f1)

### Contact

please don't hesitate to reach us if you have any doubts :

huriel.reichel@protonmail.com / huriel.reichel@uni-muenster.de
