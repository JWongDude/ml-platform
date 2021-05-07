# ---- Standard Lib Imports ----
import os
import shutil
from pathlib import Path
import tensorboard
import yaml
import glob

# ---- External Lib Imports ----
from argparse import ArgumentParser
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks.model_checkpoint import ModelCheckpoint
from pytorch_lightning.loggers import TensorBoardLogger

from PyQt5.QtCore import QObject, pyqtSignal, QThreadPool, QRunnable

import tensorboard
from tensorboard import program
import threading

# ---- Local Lib Imports ----
import app.model.pipelines.Image_Classification as ImageClassification
import app.utils as utils

# progressively import other pipelines
# import lib provides means import through string arguments

""" ---- Application Macros ----"""
WEIGHTS_DIRPATH = "app/model/weights"
PIPELINES_DIRPATH = "app/model/pipelines"
LOGS_DIRPATH = "app/model/logs"
IMAGE_CLASSIFICATION_CLASSMAP_FILENAME = "Class Map"

""" ---- Multithreading Objects ----- """
class WorkerSignals(QObject):
  started = pyqtSignal()
  finished = pyqtSignal()

class Worker(QRunnable):
  def __init__(self, pipeline, run_name, trainer, model, datamodule):
    super().__init__()
    self.signals = WorkerSignals()
    self.pipeline = pipeline
    self.run_name = run_name
    self.trainer = trainer
    self.model = model
    self.datamodule = datamodule

  def run(self):
    self.signals.started.emit()
    self.trainer.fit(self.model, self.datamodule)
    self.signals.finished.emit()

threadpool = QThreadPool()
tensorboard_thread = None

""" ---- Model API: Preprocess Panel ---- """


""" ---- Model API: Model Panel ---- """
def _set_ckpt_callback(output_directory): 
  checkpoint_callback = ModelCheckpoint(
    dirpath = output_directory, 
    save_weights_only = True,
    monitor = 'val_acc',
    mode = 'max', 
    save_top_k = 1
  )
  return checkpoint_callback

def _set_logger(pipeline, run_name):
  logger = TensorBoardLogger(save_dir='model/logs/', name = pipeline, version = run_name) # Creates a logging directory w/ experiment name
  return logger

def makeTrainingJob(pipeline, run_name, model_input, trainer_input):
  # Init argparsers for input verification
  model_parser = ArgumentParser("Model Parser")
  model_parser.add_argument('input_dirpath')
  trainer_parser = ArgumentParser("Trainer Parser")
  trainer_parser = Trainer.add_argparse_args(trainer_parser)
  
  # Verify Trainer Hyperparameters
  trainer_dict = vars(trainer_parser.parse_args(trainer_input))
  # Verify Model-Specific Hyperparameters
  if pipeline == "Image_Classification":
    model_parser = ImageClassification.datamodule.DataModule.add_model_specific_args(model_parser)
    model_parser = ImageClassification.model.Model.add_model_specific_args(model_parser)
    model_dict = vars(model_parser.parse_args(model_input))

  # Set Model-Specific Trainer Defaults:
  if pipeline == "Image Classification":
    if trainer_dict["max_epochs"] == None:
      trainer_dict["max_epochs"] = 10

  # Init Trainer and output directories of Trainer
  log_directory = LOGS_DIRPATH + '/' + pipeline + '/' + run_name
  os.mkdir(log_directory)
  trainer_dict['logger'] = _set_logger(pipeline, run_name)
  output_directory = WEIGHTS_DIRPATH + '/' + pipeline + '/' + run_name
  os.mkdir(output_directory)
  trainer_dict['callbacks'] = [_set_ckpt_callback(output_directory)]
  trainer = Trainer(**trainer_dict)

  # Perform Pipeline-Specific Actions:
  if pipeline == "Image_Classification":  # Comes with Class Map 
    # Specify number of classes in model and copy the class map to the output directory
    class_map_path = model_dict['input_dirpath'] + '/' + IMAGE_CLASSIFICATION_CLASSMAP_FILENAME + ".txt"
    model_dict['num_classes'] = utils.getNumberOfClasses(class_map_path)
    shutil.copy2(class_map_path, output_directory)

  # Init Datamodule and Model
  datamodule = ImageClassification.datamodule.DataModule(model_dict)
  model = ImageClassification.model.Model(model_dict)

  # Init Worker
  worker = Worker(pipeline, run_name, trainer, model, datamodule)

  # Return worker to Controller for any view connections
  return worker

# Call after making any view connections
def startTrainingJob(worker):
  # Run Training
  threadpool.start(worker)

def endTrainingJob(worker):
  # Transfer Training Hparams to Output Directory
  hparams_file = LOGS_DIRPATH + '/' + worker.pipeline + '/' + worker.run_name + '/' + "hparams.yaml"
  output_directory = WEIGHTS_DIRPATH + '/' + worker.pipeline + '/' + worker.run_name
  shutil.copy2(hparams_file, output_directory)

def launchTensorboard():
  tensorboard_thread = threading.Thread(target=runTb)
  tensorboard_thread.start()
  print("Loading Tensorboard...")

def runTb():
  # tb = program.TensorBoard()
  # tb.configure(argv=[None, '--logdir', LOGS_DIRPATH])
  # url = tb.launch()
  os.system('tensorboard --logdir=' + LOGS_DIRPATH)

""" ---- Model API: Inference Panel ---- """
def predict(pipeline, data_dir, ckpt_dir):
  # Type Safety 
  data_dir = str(data_dir)
  ckpt_dir = str(ckpt_dir) 

  # Get Checkpoint File in Checkpoint Path
  [ckpt_file] = glob.glob(ckpt_dir + '/' + '*.ckpt')

  if pipeline == "Image_Classification":
    # Prepare Inference Inputs
    class_mapping = utils.getClassMappingFromDirectory(ckpt_dir)
    with open(Path(ckpt_dir) / 'hparams.yaml') as file:
      params = yaml.load(file, Loader=yaml.FullLoader)

    # Run Inference
    classifier = ImageClassification.inference.Inference(class_mapping, params)
    return classifier(data_dir, ckpt_file) 