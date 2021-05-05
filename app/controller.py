# ----- controller.py -----
# Applicaition Brain and Command Center
# Processes Events, runs model, and dispatches information to the view.

# ---- Standard Lib Imports ----
from pathlib import Path
import shutil
from functools import partial
import shlex

# ---- Local Lib Imports ----
import model.api
import model.utils
import view.api
from view.api import ui_signals

""" ---- Application Macros ----"""
WEIGHTS_DIRPATH = "model/weights"
PIPELINES_DIRPATH = "model/pipelines"
LOGS_DIRPATH = "model/logs"
IMAGE_CLASSIFICATION_CLASSMAP_FILENAME = "Class Map"

""" ---- Application Data Objects ---- """
class ModelParameters:
  def __init__(self):
    # --- Model Defaults ---
    # Program Inputs
    self.data_path = None
    self.pipeline = "Image_Classification"
    self.run_name = "Experiment 1"
    # Hyperparameters
    self.model_hp = ""
    self.trainer_hp = ""
    # Model Components
    self.model = None
    self.dm = None

  def allTrainingInputsRecieved(self):
    modelInputRules = [self.data_path != None 
                      and self.pipeline != None 
                      and self.run_name != ""]
    return all(modelInputRules)

class InferenceParameters:
  def __init__(self):
    # --- Inference Defaults ---
    # Program Inputs 
    self.data_path = None
    self.pipeline = "Image_Classification" 
    self.ckpt_path = None
    # Inference Output
    self.image_directory = []   # Directory of Image Path Objects
    self.predicted_labels = []  # Directory of Labels

  def getImageDirectoryLength(self):
    return len(self.image_directory)

  def allInferenceInputsRecieved(params):
    inferenceInputRules = [params.data_path != None 
                          and params.pipeline != None 
                          and params.ckpt_path != None]
    return all(inferenceInputRules)

""" ---- Application Startup / Recovery ---- """
model_parameters = ModelParameters()
inference_parameters = InferenceParameters()

def loadApplication():
  # Load in Models / Custom Model Packages.
  # Custom Models take the same format as Models, but stored in seperate directory
  # Build up "pipeline_database"
  
  pass

def recoverApplicationState():
  # Load in pickled data objects -> application data objects
  # Call view api to display corresponding fields
  
  # Also, parse weight directories to rended those to screen:
  refreshInferenceWeights()

""" ---- Controller Setup ---- """
def connect(signal, callback):
  # connect() is a PyQt signal-and-slots function made available
  # when UI/PyQt libraries was init before controller.
  signal.connect(callback)

def connectMainWindowSignals():
  # For Developer
  # print("Callback Signals:", ui_signals)  
  # print("Registered Widgets:", ui_widgets)

  # Model Panel Signals
  connect(ui_signals['train_dirpath'], setTrainingData)
  connect(ui_signals['train_pipeline'], setTrainingPipeline)
  connect(ui_signals['modelHp'], setModelHp)
  connect(ui_signals['trainerHp'], setTrainerHp)
  connect(ui_signals['run_name'], setRunName)
  connect(ui_signals['train_button'], initializeTraining) 
  connect(ui_signals['dash_button'], launchDashboard)
  
  # Inference Panel Signals
  connect(ui_signals['inference_dirpath'], setInferenceData)
  connect(ui_signals['weight_selection'], setInferenceWeights)
  connect(ui_signals['weight_selection_rename'], renameInferenceWeights)
  connect(ui_signals['weight_selection_deletion'], deleteInferenceWeights)
  connect(ui_signals['refresh_weights'], refreshInferenceWeights)
  connect(ui_signals['inference_button'], initializeInference)
  
def connectDialogSignals():
  # TODO: Complete connections / callbacks
  # Model Panel Dialog

  # Inference Panel Dialog 
  connect(ui_signals['toggle_inference'], toggleInference)

""" -------- Control API: Model Panel ----------- """
""" Organized in order of user workflow. 
API for accessing/modifying parameter objects."""

# Triggered by Upload Training Data Button
def setTrainingData(data_path): 
  model_parameters.data_path = data_path 
  # print(data_path)

# Triggered by Select Pipeline Combobox
def setTrainingPipeline(name):
  model_parameters.pipeline = name
  # print(name)

# Triggered by Text Change in Model Parameters Line Edit
def setModelHp(text):
  model_parameters.model_hp = text
  # print(text)

# Triggered by Text Change in Trainer Parameters Line Edit
def setTrainerHp(text):
  model_parameters.trainer_hp = text
  # print(text)

# Triggered by Text Change in Run Name Line Edit
def setRunName(text):
  model_parameters.run_name = text
  # print(text)

# Triggered by "Train" Button
def initializeTraining():
  if not model_parameters.allTrainingInputsRecieved():
    error_string="Error: Please specify a data path, pipeline, and weights."
    view.api.displayTrainingErrorPresentation(error_string=error_string)

  elif not model.utils.runNameUnique(model_parameters.run_name):
    error_string="Error: Please specify a unique experiment name."
    view.api.displayTrainingErrorPresentation(error_string=error_string)

  else:
    try:
      # Format command line input as list of arguments
      model_input = [model_parameters.data_path] + shlex.split(model_parameters.model_hp)
      trainer_input = shlex.split(model_parameters.trainer_hp)
      
      # TODO: Temporary Print Feedback, remove later
      print("Model Input:", model_input)
      print("Trainer Input:", trainer_input)

      # Create Training Job 
      worker = model.api.makeTrainingJob(model_parameters.pipeline, model_parameters.run_name, model_input, trainer_input)
      
      # Connect View Updates 
      progress_string = f"Running Training Job: {model_parameters.run_name}"
      worker.signals.started.connect(partial(lambda x: view.api.displayProgressPresentation(x), progress_string))
      worker.signals.started.connect(view.api.disableTrainButton)
      end_string = f"Training Job Finished! Saved Weights: {model_parameters.run_name}"
      worker.signals.finished.connect(partial(lambda x: model.api.endTrainingJob(x), worker))
      worker.signals.finished.connect(partial(lambda x: view.api.displayProgressPresentation(x), end_string))
      worker.signals.finished.connect(view.api.enableTrainButton)

      # Start the Job
      model.api.startTrainingJob(worker)

    except:
      error_string = "Error: Please provide training data in expected format " + \
      "and provide valid hyperparameters. See the help panel for details."
      view.api.displayTrainingErrorPresentation(error_string=error_string)

def launchDashboard():
  model.api.launchTensorboard()

""" ---- Control API: Inference Panel ---- """
# Triggered by Upload Inference Data Button
def setInferenceData(dirpath):
  inference_parameters.data_path = dirpath 
  inference_parameters.image_directory = [str(image_path) for image_path in Path(dirpath).iterdir()]
  # print(dirpath)

# Triggered by Weight Panel List Widgets
def setInferenceWeights(signal):
  name, index = signal 
  inference_parameters.pipeline = name
  weight_directory = (Path(WEIGHTS_DIRPATH) / inference_parameters.pipeline).iterdir()
  pipeline_weights = [ckpt_path for ckpt_path in weight_directory]
  inference_parameters.ckpt_path = pipeline_weights[index] 
  # print(inference_parameters.ckpt_path)

# Let's just hope user does not rename to existing filename
def renameInferenceWeights(signal):
  name, index, updated_name = signal 
  if index != -1:
    weight_directory = list((Path(WEIGHTS_DIRPATH) / name).iterdir())
    weight_path = weight_directory[index]
    updated_path = Path(weight_path.parent, f"{updated_name}") 
    # Check if we are renaming the active weights
    if weight_path == inference_parameters.ckpt_path:
      inference_parameters.ckpt_path = updated_path
    weight_path.rename(updated_path)
    # print("Updated State: ", inference_parameters.ckpt_path)

def deleteInferenceWeights(signal):
  name, index, deleted_name = signal
  weight_directory = list((Path(WEIGHTS_DIRPATH) / name).iterdir())
  weight_path = weight_directory[index]
  # Check if we are deleting the active weights
  if weight_path == inference_parameters:
    inference_parameters.ckpt_path = None
  shutil.rmtree(weight_path)
  # print("Updated State: ", inference_parameters.ckpt_path)

# Triggered by Refresh Button, also called on application initialization
def refreshInferenceWeights():
  # Pass along list of strings to view
  for dirpath in Path(WEIGHTS_DIRPATH).iterdir(): 
    pipeline = dirpath.name
    weight_names = [path.stem for path in Path(dirpath).iterdir()]
    view.api.refreshInferenceWeights(pipeline, weight_names)

# Triggered by "Inference" Button
def initializeInference():
  if not inference_parameters.allInferenceInputsRecieved():
    error_string="Error: Please specify a data path, pipeline, and weights."
    view.api.displayInferenceErrorPresentation(error_string=error_string)
  else:
    try: 
      # TODO: Add Index / Label Search Functionality for quick navigation. 
      # Get Prediction 
      predictions = model.api.predict(inference_parameters.pipeline, inference_parameters.data_path, inference_parameters.ckpt_path)
      inference_parameters.predicted_labels = predictions['labels']

      # Display First Image to View
      slider_max = inference_parameters.getImageDirectoryLength()
      image_path = inference_parameters.image_directory[0]
      label = inference_parameters.predicted_labels[0]
      view.api.presentInferenceView(image_path, label, slider_max)
      
    except: 
      error_string = "Error: Please provide test data in expected format. " + \
      "See the help panel for details."
      view.api.displayInferenceErrorPresentation(error_string=error_string)    

""" ---- Control API: Inference Dialog ---- """
# Triggered by Slider 
def toggleInference(index):
  image_path = inference_parameters.image_directory[index]
  label = inference_parameters.predicted_labels[index]
  view.api.updateInferenceView(image_path, label)


"""
TODO log:
- Tensorboard Subprocess, modifying the weights/logs will modify the other.
This is easily achieved by routing the signals to one another. 
- Start new envirnoment as last try.
- Otherwise, user can open terminal themselves.

- Quality of Life Updates
- Integrate Dakota's code

"""