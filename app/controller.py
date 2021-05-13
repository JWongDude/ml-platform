# ----- controller.py -----
# Applicaition Brain and Command Center
# Processes Events, runs model, and dispatches information to the view.

# ---- Standard Lib Imports ----
import traceback
from pathlib import Path
import os
import yaml
import shutil
from functools import partial
import shlex

# ---- Local Lib Imports ----
import app.model.api as model_api
import app.utils as utils
import app.view.api as view_api
from app.view.api import ui_signals

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
    self.infer_hash = None  # For caching vs. no caching 
    self.image_directory = []   # Directory of Image Path Objects
    self.predicted_labels = []  # Directory of Labels
    # Inference Dialog
    self.slider_index = 0

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
  
  # Load in YAML application config file
  pass

def recoverApplicationState():
  # Load in pickled data objects -> application data objects
  # Call view api to display corresponding fields
  
  # TODO: Autosave applicaiton state
  # Quality of Life Inference View Startup Feedback 
  # if inference_parameters.ckpt_path == None:
  #   feedback_string = "No models trained yet! Visit Model Training to train your first model."
  #   view_api.refreshInferenceWeightFeedback(feedback_string)

  # Also, parse weight directories to rended those to screen:
  refreshDatabaseWeights()

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
  connect(ui_signals['inference_button'], initializeInference)
  connect(ui_signals['report_button'], generateReport)

  # Database Widget Signals  
  connect(ui_signals['weight_selection_rename'], renameDatabaseWeights)
  connect(ui_signals['weight_selection_deletion'], deleteDatabaseWeights)
  connect(ui_signals['refresh_weights'], refreshDatabaseWeights)

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
    error_string="Error: Please provide training data."
    view_api.displayTrainingErrorPresentation(error_string=error_string)

  elif not utils.runNameUnique(model_parameters.run_name):
    error_string="Error: Please specify a unique experiment name."
    view_api.displayTrainingErrorPresentation(error_string=error_string)

  else:
    try:
      # Format command line input as list of arguments
      model_input = [model_parameters.data_path] + shlex.split(model_parameters.model_hp)
      trainer_input = shlex.split(model_parameters.trainer_hp)
      
      # TODO: Temporary Print Feedback, remove later
      print("Model Input:", model_input)
      print("Trainer Input:", trainer_input)

      # Create Training Job 
      worker = model_api.makeTrainingJob(model_parameters.pipeline, model_parameters.run_name, model_input, trainer_input)
      
      # Connect View Updates 
      progress_string = f"Running Training Job: {model_parameters.run_name}"
      worker.signals.started.connect(partial(lambda x: view_api.displayProgressPresentation(x), progress_string))
      worker.signals.started.connect(view_api.disableTrainButton)
      end_string = f"Training Job Finished! Saving Trained Model: {model_parameters.run_name}"
      worker.signals.finished.connect(partial(lambda x: view_api.displayProgressPresentation(x), end_string))
      worker.signals.finished.connect(view_api.enableTrainButton)

      # Start the Job
      model_api.startTrainingJob(worker)

    except Exception:
      error_string = "Error: Please provide training data in expected format " + \
      "and provide valid hyperparameters."
      view_api.displayTrainingErrorPresentation(error_string=error_string)
      print(traceback.format_exc())

def launchDashboard():
  model_api.launchTensorboard()

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
  weight_directory = (Path("database") / inference_parameters.pipeline).iterdir()
  pipeline_weights = [ckpt_path for ckpt_path in weight_directory]
  inference_parameters.ckpt_path = pipeline_weights[index] 
  # print(inference_parameters.ckpt_path)

# Triggered by "Inference" Button
def initializeInference():
  if not inference_parameters.allInferenceInputsRecieved():
    error_string="Error: Please provide an image directory and selected a trained model."
    view_api.displayInferenceErrorPresentation(error_string=error_string)
  else:
    try: 
      # Calculate Directory hash for caching
      md5_hash = utils.md5_dir(inference_parameters.data_path)
      infer_hash = md5_hash + str(hash(inference_parameters.pipeline))

      # Set hash and predictions for first input directory and any new/modified input directories
      if inference_parameters.infer_hash is None or inference_parameters.infer_hash != infer_hash:  
        inference_parameters.infer_hash = infer_hash
        setInferenceData(inference_parameters.data_path)
        predictions = model_api.predict(inference_parameters.pipeline, inference_parameters.data_path, inference_parameters.ckpt_path)
        inference_parameters.predicted_labels = predictions['labels']

        # Initialize View w/ index = 0
        slider_max = inference_parameters.getImageDirectoryLength()
        image_path = inference_parameters.image_directory[0]
        label = inference_parameters.predicted_labels[0]
        view_api.presentInferenceView(image_path, label, slider_max)

        # Reset the Report Button Feedback 
        view_api.clearReportButtonFeedback()

      # Otherwise, hashes are equal. Use previously computed predictions
      else:
        # Initialize View w/ last index
        slider_max = inference_parameters.getImageDirectoryLength()
        image_path = inference_parameters.image_directory[inference_parameters.slider_index]
        label = inference_parameters.predicted_labels[inference_parameters.slider_index]
        view_api.presentInferenceView(image_path, label, slider_max)

      # Clear any error string
      view_api.displayInferenceErrorPresentation(error_string="")
      print("Loading Image Explorer...")

    except Exception:
      error_string = "Error: Please provide test data as plain image directory."
      view_api.displayInferenceErrorPresentation(error_string=error_string)
      print(traceback.format_exc())    

""" ---- Control API: Inference Dialog ---- """
# Triggered by Slider 
def toggleInference(index):
  inference_parameters.slider_index = index
  image_path = inference_parameters.image_directory[index]
  label = inference_parameters.predicted_labels[index]
  view_api.updateInferenceView(image_path, label)

""" ---- Control API: Database Utils ---- """
# Let's just hope user does not rename to existing filename
def renameDatabaseWeights(signal):
  name, index, updated_name = signal 
  if index != -1:
    weight_directory = list((Path("database") / name).iterdir())
    weight_path = weight_directory[index]
    updated_path = Path(weight_path.parent, f"{updated_name}") 
    # Check if we are renaming the active weights
    if weight_path == inference_parameters.ckpt_path:
      inference_parameters.ckpt_path = updated_path
    weight_path.rename(updated_path)
    # print("Updated State: ", inference_parameters.ckpt_path)

def deleteDatabaseWeights(signal):
  name, index, deleted_name = signal
  weight_directory = list((Path("database") / name).iterdir())
  weight_path = weight_directory[index]
  # Check if we are deleting the active weights
  if weight_path == inference_parameters:
    inference_parameters.ckpt_path = None
  shutil.rmtree(weight_path)
  # print("Updated State: ", inference_parameters.ckpt_path)

# Triggered by Refresh Button, also called on application initialization
def refreshDatabaseWeights():
  # Pass along list of strings to view
  for dirpath in Path("database").iterdir(): 
    pipeline = dirpath.name
    weight_names = [path.stem for path in Path(dirpath).iterdir()]
    view_api.refreshDatabaseWeights(pipeline, weight_names)


""" ---- Control API: Output Utils ---- """
"""
Report Format:
---- <Experiment Name>_Report.txt ----
Experiment Name: <Experiment Name>
Model Type: <Model Type>

Model Training: 
Training Hyperparameters: 
  (List hyperparameters from yaml file)
Training Metrics: 
  See dashboard, please print visualizations from browser

Model Prediction: 
Image Directory: <Image Directory Name>
<image name>  <prediction>
<image name>  <prediction>
<image name>  <prediction>
...
"""
def generateReport():
  # Get the location of downloads folder
  downloads_path = os.path.join(os.getenv('USERPROFILE'), 'Downloads')
  
  # Get valid file name for report
  counter = 0
  file_name = f'{model_parameters.run_name}_Report.txt'
  file_path = os.path.join(downloads_path, file_name)
  while os.path.isfile(file_path):
    counter += 1
    file_name = f'{model_parameters.run_name}_Report ({counter}).txt'
    file_path = os.path.join(downloads_path, file_name)

  # Access Model Info from Current Experiment
  with open(Path(inference_parameters.ckpt_path) / 'hparams.yaml') as file:
    params = yaml.load(file, Loader=yaml.FullLoader)
  # params is a map of yaml entries
  input_dirpath = params.pop('input_dirpath', None)

  # Write report
  with open(file_path, 'w') as f:
    # Heading
    f.write(f"Experiment Name: {model_parameters.run_name} \n")
    f.write(f"Model Type: {model_parameters.pipeline} \n")
    f.write("\n")

    # Training Information
    f.write("Model Training Parameters: \n")
    f.write(f"Training Directory: {input_dirpath} \n")
    for param, value in params.items():
      f.write(f"{param}: " + str(value) + "\n")
    f.write("Please reference model training dashboard for training metrics. \n")
    f.write("\n")

    # Prediction Information
    f.write("Model Predictions: \n")
    f.write(f"Image Directory: {inference_parameters.data_path} \n")
    if inference_parameters.pipeline == "Image_Classification":
      
      for image, label in zip(inference_parameters.image_directory,
                              inference_parameters.predicted_labels):
        f.write(f"{Path(image).stem}   {label} \n")