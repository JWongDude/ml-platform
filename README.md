# ml-platform 
Low-Code ML-Platform for Computer Vision in collaboration with Boeing.  

## Motivation 
This project automates model training of image classification and object detection models in an end-to-end manner. <br>
Simply provide the training data and platform handles the rest!

## Installation 
### Windows: 
Install [Python](https://www.python.org/downloads/), [Git](https://git-scm.com/downloads) 

Clone Repository and Setup Application Environment: 
```bash
git clone https://github.com/JWongDude/ml-platform.git
python -m venv .venv

.venv/Scripts/Activate.ps1  # Powershell 
source .venv/Scripts/activate  # Shell

pip install -r requirements.txt
python app.py 
```

## Usage
### Windows:
Navigate to Project Directory `cd <path/to/project/directory>`, <br>
activate virtualenv if needed `.\venv\Scripts\activate`, <br>
and run entrypoint `python app.py`.<br>
