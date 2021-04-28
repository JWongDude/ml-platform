# ---- External Lib Imports ----
from PyQt5.QtWidgets import(
  QFrame, QSpacerItem, QSizePolicy, QHBoxLayout, QVBoxLayout)

# ---- Local Lib Imports ----
from view.widgets import (Dialog, Heading, HSeperationLine, ListWidget, 
  Selector, Button, UploadWidget, Image, Slider, LineEditLayout, TextBox, ListWidgetSelector
)
import view.api as view_api

""" --- Custom Inference Panel Widgets --- """
class WeightPanel(QFrame):
  def __init__(self, names):
    super().__init__()
    # Init Widgets
    self.lw_selector = ListWidgetSelector(select_names=names, signal_key="weight_selection", 
                                                          update_key="update_weight_list")
    self.button = Button(signal_key="refresh_weights")
    self.button.setText("Refresh")
    self.feedback = TextBox("", wordWrap=False)
    self.file = ""

    # Footer Layout
    footer_layout = QHBoxLayout()
    footer_layout.addWidget(self.feedback)
    footer_layout.addItem(QSpacerItem(40, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))
    footer_layout.addWidget(self.button)

    # Layout
    layout = QVBoxLayout()
    layout.addWidget(self.lw_selector)
    layout.addLayout(footer_layout)
    self.setLayout(layout)

    # Connect the refresh button signal to a feedback label
    self.lw_selector.selection.connect(self._updateFeedbackFromSelection)
    # Connect the rename signal to the feedback label
    self.lw_selector.renamedFile.connect(self._updateFeedbackFromRename)
    # Connect the delete signal to the feedback label 
    self.lw_selector.deletion.connect(self._updateFeedbackFromDeletion)

  def _updateFeedbackFromSelection(self):
    self.file = self.lw_selector.getCurrentWidget().getCurrentText()
    self.feedback.setText("Current Selection: " + self.file)

  def _updateFeedbackFromRename(self, signal):
    name, index, updated_name = signal 
    self.file = updated_name
    if index != -1:
      self.feedback.setText("Current Selection: " + self.file)
  
  def _updateFeedbackFromDeletion(self, signal):
    name, index, deleted_name = signal
    if self.file == deleted_name:
      self.file = ""
      self.feedback.setText("")

class InferenceDialog(Dialog):
  def __init__(self, image_path, label, slider_max):
    super().__init__("Explorer")
    # Init Widgets
    self.image = Image(image_path, update_key="inference_image")
    self.label = LineEditLayout(label_text="Label: ", edit_text=label, update_key="inference_label")
    self.label.line_edit.setReadOnly(True)
    self.slider = Slider(self, 0, slider_max, signal_key="toggle_inference", update_key="update_slider_length")
    self.slider.setFocus(True)

    # Layout
    layout = QVBoxLayout()
    layout.addWidget(self.image)
    layout.addLayout(self.label)
    layout.addWidget(self.slider)
    self.setLayout(layout)
  
    # Register Update Function
    view_api.add_to_update_map(self.updateDialog, update_key="toggle_inference")

  def setSliderLength(self, length):
    self.slider.setMaximum(length - 1) # Maximum value corresponds to maximum index!

  def updateDialog(self, image_path, label):
    self.image.updateImage(image_path)
    self.label.updateEditText(label)

class InferenceLaunchpad(QFrame):
  def __init__(self):
    super().__init__()
    # Init Launchpad Widgets
    inference_button = Button(signal_key="inference_button")
    inference_button.setText("Open Explorer")
    inference_feedback = TextBox("", update_key="update_inference_feedback")

    # Layout
    layout = QVBoxLayout()
    layout.addWidget(inference_button)
    layout.addWidget(inference_feedback)
    self.setLayout(layout)

    # Register Launchpad Update Function
    view_api.add_to_update_map(self.initAndlaunchDialog, update_key="launch_inference_dialog")

    # Initialize Dialog Widget once! 
    # Blank, Placeholder State:
    image_path = ""
    label = ""
    slider_max = 10
    self.dialog = InferenceDialog(image_path, label, slider_max)
    
  # Launchpad Method
  def initAndlaunchDialog(self, image_path, label, slider_max): 
    self.dialog.updateDialog(image_path, label)
    self.dialog.setSliderLength(slider_max)
    self.dialog.exec_()

class InferenceView(QFrame):
  def __init__(self):
    super().__init__()
    
    # Build Custom Widgets
    upload_widget = UploadWidget(signal_key="inference_dirpath")
    # weight_panel = WeightPanel()
    names = ["Image_Classification", "Object_Detection", "Object_Segmentation"]
    weight_panel = WeightPanel(names)
    inference_launchpad = InferenceLaunchpad()

    # Layout
    layout = QVBoxLayout()
    layout.addWidget(Heading(" Model Inference", 20))
    layout.addWidget(HSeperationLine())
    layout.addWidget(Heading(" Upload Inference Data", 12))
    layout.addWidget(upload_widget)
    layout.addWidget(HSeperationLine())
    layout.addWidget(Heading(' Select Pipeline Weights', 12))
    layout.addWidget(weight_panel)
    layout.addWidget(HSeperationLine())
    layout.addWidget(Heading(' Launch Inference', 12))
    layout.addWidget(inference_launchpad)
    layout.addItem(QSpacerItem(20, 120, QSizePolicy.Preferred, QSizePolicy.Expanding))
    self.setLayout(layout)