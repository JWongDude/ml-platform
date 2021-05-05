# ---- External Lib Imports ----
from PyQt5.QtWidgets import(
  QFrame, QHBoxLayout, QVBoxLayout
)

# ---- Local Lib Imports ----
from app.view.widgets import (HSeperationLine, LineEditLayout, Button, TextBox, 
  UploadWidget, Selector, Heading, Spacer 
)

""" --- Custom Model Panel Widgets --- """
class HyperparameterEdit(QFrame):
  def __init__(self):
    super().__init__()
    # Line Edits for Hyperparameter Tuning
    modelHpLayout = LineEditLayout(label_text="Model Hyperparameters:   ", 
                                          edit_text="", signal_key="modelHp")
    trainerHpLayout= LineEditLayout(label_text="Trainer Hyperparameters: ", 
                                          edit_text="", signal_key="trainerHp")

    # Layout
    layout = QVBoxLayout()
    layout.addLayout(modelHpLayout)
    layout.addLayout(trainerHpLayout)
    self.setLayout(layout)

class ButtonPanel(QFrame):
  def __init__(self):
    super().__init__()
    # Init Buttons
    train_button = Button(signal_key="train_button", update_key="update_train_button")
    train_button.setText("Train")
    dash_button = Button(signal_key="dash_button")
    dash_button.setText("Open Dashboard")

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
    widget_map = {"Image_Classification": TextBox("\nLorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. \n \n"),
                  "Object_Detection": TextBox("--- Object Detection Description Here ---"),
                  "Image_Segmentation": TextBox("--- Image Segmentation Description Here ---")}
    model_selector = Selector(widget_map, signal_key="train_pipeline")
    hp_edit = HyperparameterEdit()
    runner = Runner()

    layout = QVBoxLayout()
    layout.addWidget(Heading(' Model Training', 20))
    layout.addWidget(HSeperationLine())
    layout.addWidget(Heading(' Upload Training Data', 12))
    layout.addWidget(upload_widget)
    layout.addWidget(HSeperationLine())
    layout.addWidget(Heading(' Select Pipeline', 12))
    layout.addWidget(model_selector)
    layout.addWidget(hp_edit)
    layout.addWidget(HSeperationLine())
    layout.addWidget(Heading(' Submit Training Run', 12))
    layout.addWidget(runner)
    layout.addItem(Spacer(20, 120))
    self.setLayout(layout)