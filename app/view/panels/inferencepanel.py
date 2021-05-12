# ---- External Lib Imports ----
from pathlib import Path
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import(
  QFrame, QScrollArea, QSpacerItem, QSizePolicy, QHBoxLayout, QVBoxLayout, QWidget)

# ---- Local Lib Imports ----
from app.view.widgets import (Dialog, Heading, HSeperationLine, ListWidget, 
  Selector, Button, Spacer, UploadWidget, Image, Slider, LineEditLayout, TextBox, ListWidgetSelector
)
import app.view.api as view_api

""" --- Custom Inference Panel Widgets --- """
class WeightPanel(QFrame):
  def __init__(self, names):
    super().__init__()
    # Init Widgets
    self.lw_selector = ListWidgetSelector(select_names=names, signal_key="weight_selection", 
                                                          update_key="update_weight_list")
    self.button = Button(signal_key="refresh_weights")
    self.button.setText("Refresh")
    self.feedback = TextBox("", wordWrap=False, update_key="update_weight_panel_feedback")
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
    super().__init__("Image Explorer")
    # Init Widgets
    self.setFrameRect(QRect(0, 0, 1000, 1000))
    self.report_button = Button(signal_key="report_button")
    self.report_button.setText("Generate Report")
    self.image_name = TextBox("")
    self.feedback = TextBox("", update_key="report_button_feedback")
    self.feedback.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    self.image = Image(image_path, update_key="inference_image")
    self.label = LineEditLayout(label_text="Predicted Label: ", edit_text=label, update_key="inference_label")
    self.label.line_edit.setReadOnly(True)
    self.slider = Slider(self, 0, slider_max, signal_key="toggle_inference", update_key="update_slider_length")
    self.slider.setFocus(True)

    # Report Feedback 
    feedback_string = "Report Generated! Please Check Downloads Folder."
    self.report_button.clicked.connect(lambda: self.feedback.setText(feedback_string))

    # Obnoxious Scroll Bar Code
    self.scroll_area = QScrollArea()
    self.widget = QWidget()
    self.widget.setMaximumSize(1400, 1400)
    self.image_layout = QVBoxLayout()
    self.image_layout.addWidget(self.image)
    self.widget.setLayout(self.image_layout)
    self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    self.scroll_area.setWidgetResizable(True)
    self.scroll_area.setWidget(self.widget)

    # Header
    header = QHBoxLayout()
    header.addWidget(Heading("Image Explorer"))
    header.addSpacerItem(Spacer(height=20))
    header.addWidget(self.report_button)

    # Subheader
    subheader = QHBoxLayout()
    subheader.addWidget(self.image_name)
    subheader.addSpacerItem(Spacer(height=20))
    subheader.addWidget(self.feedback)

    # Layout
    layout = QVBoxLayout()
    layout.addLayout(header)
    layout.addLayout(subheader)
    layout.addWidget(self.scroll_area)
    layout.addLayout(self.label)
    layout.addWidget(self.slider)
    self.setLayout(layout)
  
    # Register Update Function
    view_api.add_to_update_map(self.updateDialog, update_key="toggle_inference")

  def setSliderLength(self, length):
    self.slider.setMaximum(length - 1) # Maximum value corresponds to maximum index!

  def updateDialog(self, image_path, label):
    image_name = Path(image_path).stem
    self.image_name.setText("Image Name: " + image_name)
    self.image.updateImage(image_path)
    self.label.updateEditText(label)

class InferenceLaunchpad(QFrame):
  def __init__(self):
    super().__init__()
    # Init Launchpad Widgets
    inference_button = Button(signal_key="inference_button")
    inference_button.setText("Open Image Explorer")
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
    self.dialog.run_dialog()

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
    layout.addWidget(Heading(" Model Prediction", font_size=20))
    layout.addWidget(HSeperationLine())
    layout.addWidget(Heading(" 1) Upload Image Directory", font_size=12))
    layout.addWidget(upload_widget)
    layout.addWidget(HSeperationLine())
    layout.addWidget(Heading(' 2) Select Trained Model', font_size=12))
    layout.addWidget(weight_panel)
    layout.addWidget(HSeperationLine())
    layout.addWidget(Heading(' 3) View Model Results', font_size=12))
    layout.addWidget(inference_launchpad)
    layout.addItem(QSpacerItem(20, 150, QSizePolicy.Preferred, QSizePolicy.Expanding))
    self.setLayout(layout)