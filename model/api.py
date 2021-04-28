# ---- External Lib Imports ----
from argparse import ArgumentParser
from pytorch_lightning import Trainer
from pytorch_lightning.callbacks.model_checkpoint import ModelCheckpoint
from pytorch_lightning.loggers import TensorBoardLogger

from PyQt5.QtCore import QObject, pyqtSignal, QThreadPool, QRunnable

# ---- Local Lib Imports ----
import model.pipelines.Image_Classification as ImageClassification
import model.utils as utils

# progressively import other pipelines
# import lib provides means import through string arguments

""" ---- Application Data Objects ---- """
class WorkerSignals(QObject):
  started = pyqtSignal()
  finished = pyqtSignal()

class Worker(QRunnable):
  def __init__(self, trainer, model, datamodule):
    super().__init__()
    self.signals = WorkerSignals()
    self.trainer = trainer
    self.model = model
    self.datamodule = datamodule

  def run(self):
    self.signals.started.emit()
    self.trainer.fit(self.model, self.datamodule)
    self.signals.finished.emit()

class Active:
  def __init__(self) -> None:
    self.thread = None
    self.worker = None
    
threadpool = QThreadPool()

""" ---- Model API: Preprocess Panel ---- """


""" ---- Model API: Model Panel ---- """
def _set_ckpt_callback(pipeline, run_name): 
  checkpoint_callback = ModelCheckpoint(
    dirpath = 'model/weights/' + pipeline,
    save_weights_only = True,
    filename = run_name + '_{epoch:02d}_{val_loss:.2f}',
    monitor = 'val_acc',
    mode = 'max', 
    save_top_k = 1
  )
  return checkpoint_callback

def _set_logger(pipeline, run_name):
  logger = TensorBoardLogger(save_dir='model/logs/' + pipeline, name = run_name)
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

  # Init Trainer 
  trainer_dict['callbacks'] = [_set_ckpt_callback(pipeline, run_name)]
  trainer_dict['logger'] = _set_logger(pipeline, run_name)
  trainer = Trainer(**trainer_dict)

  # Add Pipeline-Specific Parameters
  if pipeline == "Image_Classification":
    # Add number of classes to dictionary
    model_dict['num_classes'] = utils.numberOfClasses(model_dict['input_dirpath'] + '/' + "train")

  # Init Datamodule and Model
  datamodule = ImageClassification.datamodule.DataModule(model_dict)
  model = ImageClassification.model.Model(model_dict)

  # Init Worker
  worker = Worker(trainer, model, datamodule)

  # Return worker to Controller for any view connections
  return worker

# Call after making any view connections
def startTrainingJob(worker):
  threadpool.start(worker)

""" ---- Model API: Inference Panel ---- """
def predict(pipeline, data_path, ckpt_path):
  if pipeline == "Image_Classification":
    classifier = ImageClassification.inference.Inference(transform = datamodule.transform['val'], 
                                              class_mapping = datamodule.class_mapping)
    return classifier(data_path, ckpt_path) 