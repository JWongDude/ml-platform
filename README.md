# ml-platform 
Low-Code ML-Platform for Computer Vision in collaboration with Boeing.  

## Motivation 
This project automates model training of image classification and object detection models in an end-to-end manner. Simply provide the training data and platform handles the rest!

## Installation 
### Windows: 
Install [Python](https://www.python.org/downloads/), [Git](https://git-scm.com/downloads) 

Tested to be Functional on **Python version 3.8.8**

Clone Repository and Setup Application Environment: 
```bash
git clone https://github.com/JWongDude/ml-platform.git
python -m venv .venv

.venv/Scripts/Activate.ps1  # Powershell 
source .venv/Scripts/activate  # Shell

pip install -r requirements.txt
python app.py 
```

As the last installation step, please make an empty directory called "database" in the same place as app.py. Please make the folder with the following subdirectorty structure: 

```bash
- database
    |-Image_Classification
    |-Object_Detection
    |-Object_Segmentation
```
All outputs (trained models, metrics) of the platform will be stored inside of this folder. You will need the database folder to save the model outputs. 

## Usage
### Windows:
Navigate to Project Directory `cd <path/to/project/directory>`, <br>
activate virtualenv if needed `./venv/Scripts/activate`, <br>
and run entrypoint `python app.py`.<br>

If your computer has a GPU, please head to the official [Pytorch](https://pytorch.org/get-started/locally/) website and retrieve the pytorch version compatible with your hardware. Install this pytorch into your virtual environment.

```bash 
# Ex, for CUDA 10.2, run the following: 
pip3 install torch==1.8.1+cu102 torchvision==0.9.1+cu102 torchaudio===0.8.1 -f https://download.pytorch.org/whl/torch_stable.html

```
If necessary, update the GPU Driver at [Nvidia](https://www.nvidia.com/Download/index.aspx)
(The platform will not let you train on an old GPU Driver with an error message to this link.
Attempt to train and follow the error message if it appears.) 

With those instructions completed, you should have the platform up-and-running. 

**Training a Model**: <br>
- Image Classification: <br>
The training image directory expected format is organized as the following:
```bash
<your directory name>
  |- train
    |- <Class 1 name>
      |- <place corresponding images here>
    |- <Class 2 name>
    |- ...
    |- <Class n name>
  |- valid
    |- <Class 1 name>
    |- <Class 2 name>
    |- ...
    |- <Class n name>
  Class Map.txt
```
The image data will require an accompanying text file called "Class Map.txt" inside the training image directory. Simply number your classes in the format shown: <br>
```bash
<Class 0 name>: 0
<Class 1 name>: 1
...
<Class n name>: n
```
For example: 
```bash
giraffe: 0
peacock: 1
flamingo: 2
```
It does not matter how you order the classes. The underlying nueral network produces an integer output, so this file provides a translation of what each integer means. 

**Sharing a Model**: <br>

If you would like to share a trained model to another person using the platform, this is simply done by exporting your experiment into the reciever's database folder. For example, 
say I have a trained an image classification model called "Experiment 1". You will find a new folder inside the Image_Classification folder called "Experiment 1", which contains all the model's details. Send this folder to the recipient and place in the recipient's Image_Classification folder to complete sharing. 

## Platform Tour
### Model Training Panel 
![ML Platform Model Panel](https://user-images.githubusercontent.com/54962990/118059403-511e7d00-b345-11eb-9fe5-468c96373097.PNG)

Features include: 
- Selection between Image Classification, Object Detection, and Object Segmentation. 
- Hyperparameter Configuration
- GPU Support 
- Tensorboard Logging 

### Model Prediction Panel 
![ML Platform Prediction Panel](https://user-images.githubusercontent.com/54962990/118061178-4665e700-b349-11eb-933f-aae6b5f65e58.PNG)

Features include:
- Point and Click Selection of Trained Models
- Rename and Delete Functionality
- Image Explorer for Visualization of Model Results.

### Image Explorer
![ML Platform Image Explorer](https://user-images.githubusercontent.com/54962990/118059503-888d2980-b345-11eb-98ea-5f52827fead5.PNG)

Features include: 
- Resizeable window, for framing any size input
- Report Generation containing information of trained model metrics and model predictions. 

### Tutorial Video
 ----- Coming Soon -----