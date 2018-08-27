# Building Recognition with Convolutional Neural Networks From a Virtual Scene #

Bachelor Thesis - Project files for my bachelor thesis. 

This repository contains the code that was developed for the implementation of the given task.

For recognizing buildings from a virtual scene a CNN called [U-Net](https://lmb.informatik.uni-freiburg.de/people/ronneber/u-net/) was used. The recognition tasked was solved with a segmentation. 
This example shows how the networks basically works.

This implementation was transfered from a biomedical task developed by [Pietz](https://github.com/pietz/knee-mri-segmentation)   

![Overview](https://github.com/DevNesh/BA_SceneSimulation/blob/master/readme_ressources/overview.png)   

Based on the following virtual model:

![Wooden Model](https://github.com/DevNesh/BA_BuildingRecognitionWithCNN/blob/master/readme_ressources/screenshot_woodenModel.PNG)   


## Summary ##
 The repository is divided into the following parts:

#### ./city_skyline ####
Unity Project, contains a virtual scene that looks like a wooden model. A camera algorithm is developed, that puts the camera on different positions around the model and takes two pictures of the scene from this position 
* **ScreenshotHandler, CameraHandler** 
    * a normal picture with the wooden model
    * a picture where the selected buliding is marked with a red material 

* a camera flight was made, where the camera flies on a defined spline root around the scene. The spline root is defined in the Hierachy. The necessary scripts are added to the *Main Camera*.

#### ./data_processing ####
Python implementations for prepocessing the images for the training of the neural network. 
* **data_preprocessing.py**, a module that can be used for creating the ground truth images based on the taken screenshots and the input pictures. 
* **data_augmentation.py**, a module that can be used to add data augmentation to the dataset.
* **data_splitting.py**, a module that can be used for splitting the data into train, test and validation set. 

#### ./neural_networks ####
Jupyter Notebook implementations that are handeling different notebooks for working with a neural Network.
* **train_network_big.ipynb**, notebook for training a U-Net with Keras DataGenerators
* **train_network_small.ipynb**, notebook for training a U-Net without Keras DataGenerators
* **train_network_multiclass_small.ipynb**, notebook for training a mulitisegmentation U-Net
* **evaluation.ipynb**, notebook for loading a trained U-Net and evaluating this on a testset
* **prediction_small.ipynb**, notebook for creating predicitons from a trained U-Net.
* **snippet.ipynb**, notebook with incoherent code snippets

#### ./video_prediction_example.mp4 ####
An example of how the network performs on a video, that should simulate the user interactions. 

## Prerequisites
For this implementation several things are needed: 
* Unity 
* Python 3.6
* Keras 
* OpenCV 

## Instruction ##

### Unity ### 
To create a dataset for a specific building do the following steps: 
1. Open Unity and load the *city_skyline* project
2. Load the *wooden_model* Scene. You will find this scene under: *Assets/Scenes/wooden_model*
3. Click on the *Main Camera* Object in the Hierarchy and look at the *Screenshot Handler (Script)* in the Inspector.

![ScreenshotHandler](https://github.com/DevNesh/BA_SceneSimulation/blob/master/readme_ressources/screenshot_unity1.PNG)
* Put the reference from the building you want to mark into the *Marked Object* field. Open the * Buildings* Gameobject in the Hierachy and drag and drop one of the child elements to the *Marked Object* field in the Inspector (marked in red)

    *  After that create some folders on your explorer where the images can be saved. A structure like this is highly recommended:  
    
    ```
    .
    ├──  Dataset_BuildingX
    |    ├── Original
    |    └── Marked
    └── ...
    ```

    * Copy the path of the *Original* and *Marked* folder in the expected fields. (marked red)

4. Click on the *Main Camera* Object in the Hierarchy and look at the *Camera Handler (Script)* in the Inspector.

![CameraHandler](https://github.com/DevNesh/BA_SceneSimulation/blob/master/readme_ressources/screenshot_unity2.PNG)

* Justify the resolutions for the camera positions by setting the values marked in red
* Justify the viewpoints by setting the *Cube Devisions* marked in blue
* For debugging and visualisation the camera positions and viewpoints activate the checkbox marked in green. If checked, spheres will be created at all the defined positions and no screenshots will be saved.

5. Build the scene and start the application. A resolution of 1024x768 is recommended. By starting the algorithm, two screenshots with the same name will be created and every image (original or marked) will be saved in the associated defined folder.

    * If the amount of *Cube Devisions* is 1 and you want a dataset where the camera also looks in the middle of the scene, press **u** , wait until the screenshot taking is done. After that press **i** for creating the screenshots for the next 8 viewpoints

    * If the amount of *Cube Devisions* is higher than one, only press **i** and wait until the alogrithm is done. 


## Data Preprocessing ##
To prepare the data for the neural network do the following steps:

1. Add a new file structure, where the new images can be saved. It is highly recommended to use the following structure: 
    ```
        .
        ├── Dataset_BuildingX
        |   ├── Original
        |   ├── Marked
        |   └── train
        |       ├── images
        |       |   └── data
        |       └── masks 
        |           └── data
        |    
        └── ...
    ```
2. Open the *data_preprocessing.py* file and change the follwoing variables to your specific path values: 

    ```
    ...
    inputPathOriginal = '/.../.../.../Datenset_X/Original'
    inputPathMarked = '/.../.../.../Datenset_X/Marked'

    outputPathMask = '/.../.../.../Datenset_X/train/masks/data'
    outputPathOriginal = '/.../.../.../Datenset_X/train/images/data'
    ...
    ```

3. Save the file and execute the python script. All images will be saved in the new directories.

    ```
    C:\Users\example\Path\To\File> python data_preprocessing.py
    ```

4. Open the *data_augmentation.py* file and change the following variable to your specific path to the images: 

    ```
    ...
    inputPath = '/.../.../.../Datenset_X/train/images/data'
    ...
    ```

5. Save the file and execute the python script. Data augmentation will be added to your data.

    ```
    C:\Users\example\Path\To\File> python data_augmentation.py
    ```

6. For splitting the data into train/test/validate, create new directories like this:
    ```
        .
        ├── Dataset_BuildingX
        |   ├── Original
        |   ├── Marked
        |   ├── train
        |   |   ├── images
        |   |   |   └── data
        |   |   └── masks 
        |   |       └── data
        |   ├── test
        |   |   ├── images
        |   |   |   └── data
        |   |   └── masks 
        |   |       └── data
        |   └── validate
        |       ├── images
        |       |   └── data
        |       └── masks 
        |           └── data
        |    
        └── ...
    ```

7. Open the *data_splitting.py* file and change the following variable to your specific name of the dataset folder:

    ```
    ...
    foldername = 'Datenset_BlockX'
    ...
    ```

8. Save the file and execute the python script. Your data will be splitted and is ready for training the U-Net

    ```
    C:\Users\example\Path\To\File> python data_splitting.py
    ```

## Neural Network ##
For training a neural network it is recommended to use the *train_network_big.ipynb* Jupyter notebook. It is implemented with the Keras DataGenerator for handeling a big size of images and only loads a batch of images in time. This is more efficient and your task will not run into memory problems.

* Open the notebook 
* Set the values in the second cell 

 ![NeuralNetwork Cell 2](https://github.com/DevNesh/BA_SceneSimulation/blob/master/readme_ressources/screenshot_neuralnetwork.PNG)

* Execute every cell step by step and change the parameter to your usecase