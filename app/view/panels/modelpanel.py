# ---- External Lib Imports ----
from typing import Text
from PyQt5.QtWidgets import(
  QFrame, QHBoxLayout, QVBoxLayout
)

# ---- Local Lib Imports ----
from app.view.widgets import (HSeperationLine, LineEditLayout, Button, ListWidgetSelector, TextBox, 
  UploadWidget, Selector, Heading, Spacer, Dialog
)

""" --- Custom Model Panel Widgets --- """
class ModelText(QFrame):
  def __init__(self, modelHp=None, trainerHp=None):
    super().__init__()
    # Init Widgets
    self.model_header = Heading("Default Model Hyperparameters", 8, underline=True)
    self.model_hp = TextBox(modelHp)
    self.trainer_header = Heading("Default Trainer Hyperparameters", 8, underline=True)
    self.trainer_hp = TextBox(trainerHp)

    # Layout
    layout = QHBoxLayout()
    left = QVBoxLayout()
    left.addWidget(self.model_header)
    left.addWidget(self.model_hp)
    layout.addLayout(left)
    right = QVBoxLayout()
    right.addWidget(self.trainer_header)
    right.addWidget(self.trainer_hp)
    layout.addLayout(right)
    self.setLayout(layout)

class HyperparameterEdit(QFrame):
  def __init__(self):
    super().__init__()
    # Init Widgets
    text = TextBox("To override the default hyperparameters, please provide a sequence of flags.")
    example = TextBox("Ex: --batch_size 64 --lr 1e-5\n")
    modelHpLayout = LineEditLayout(label_text="Model Hyperparameters:   ", 
                                          edit_text="", signal_key="modelHp")
    trainerHpLayout= LineEditLayout(label_text="Trainer Hyperparameters: ", 
                                          edit_text="", signal_key="trainerHp")

    # Layout
    layout = QVBoxLayout()
    layout.addWidget(text)
    layout.addWidget(example)
    layout.addLayout(modelHpLayout)
    layout.addLayout(trainerHpLayout)
    self.setLayout(layout)

class ButtonPanel(QFrame):
  def __init__(self):
    super().__init__()
    # Init Buttons, Log Directory Popup
    train_button = Button(signal_key="train_button", update_key="update_train_button")
    train_button.setText("Train")
    dash_button = Button(signal_key="dash_button")
    dash_button.setText("Open Dashboard")

    # Layout
    layout = QHBoxLayout()
    layout.addWidget(train_button)
    layout.addWidget(dash_button)
    self.setLayout(layout)

class Runner(QFrame):
  def __init__(self):
    super().__init__()
    # Init Widgets
    run_name = LineEditLayout(label_text="Experiment Name: ", 
                                      edit_text="Experiment 1", signal_key="run_name") 
    buttons = ButtonPanel()
    train_feedback = TextBox("", update_key="update_train_feedback")

    # Layout
    layout = QVBoxLayout()
    layout.addLayout(run_name)
    layout.addWidget(buttons)
    layout.addWidget(train_feedback)
    self.setLayout(layout)

""" --- Model Panel Widget --- """
class ModelView(QFrame):
  def __init__(self):
    super().__init__()

    # Build Custom Widgets:
    upload_widget = UploadWidget(signal_key="train_dirpath")

    self.ic = ModelText(modelHp="--length 224           --width 224 \n" +
                                "--batch_size 32       --num_workers 2 \n" +
                                "--lr 1e-3 ",
                       trainerHp="--gpus 0           --max_epochs 10\n \n")

    self.od = ModelText(modelHp="--one \n--two\n--three", trainerHp="--four\n --five\n --six")
    self.iseg = ModelText(modelHp="--one \n--two\n--three", trainerHp="--four\n --five\n --six")

    widget_map = {"Image_Classification": self.ic,
                  "Object_Detection": self.od,
                  "Image_Segmentation": self.iseg}
    model_selector = Selector(widget_map, signal_key="train_pipeline")
    hp_edit = HyperparameterEdit()
    runner = Runner()

    # Layout
    layout = QVBoxLayout()
    layout.addWidget(Heading(' Model Training', font_size=20))
    layout.addWidget(HSeperationLine())
    layout.addWidget(Heading(' 1) Upload Training Data', font_size=12))
    layout.addWidget(upload_widget)
    layout.addWidget(HSeperationLine())
    layout.addWidget(Heading(' 2) Select Model Type', font_size=12))
    layout.addWidget(model_selector)
    layout.addWidget(HSeperationLine())
    layout.addWidget(Heading(' Optional: Modify Hyperparameters', font_size=12))
    layout.addWidget(hp_edit)
    layout.addWidget(HSeperationLine())
    layout.addWidget(Heading(' 3) Submit Training Run', font_size=12))
    layout.addWidget(runner)
    layout.addItem(Spacer(20, 180))
    self.setLayout(layout)