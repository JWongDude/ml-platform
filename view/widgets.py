# ---- Standard Lib Imports ----
from pathlib import Path

# ---- External Lib Imports ----
# Utility Widgets
from PyQt5.QtWidgets import(
  QDialog, QFileDialog, QComboBox, QLineEdit, QListWidget, 
  QPushButton, QLabel, QSlider, QStackedWidget, QAction)

# Organization Widgets
from PyQt5.QtWidgets import(
  QFrame, QStackedWidget, QSpacerItem, QSizePolicy, QVBoxLayout, QFormLayout)
from PyQt5.QtCore import (Qt, QSize, pyqtSignal)

# Style Widgets
from PyQt5.QtGui import (QIcon, QFont, QPixmap)

# ---- Local Lib Imports ----
import view.api as view_api

""" ---- Widget Library: Style / Conventions ---- """
""" Widget library defines set of widget 
primitives and widget composites for reuse. 
Each widget defines defaults settings and registration to 
signal and update maps. Singal and update maps establish
communication with the control api, such that all ui events 
and update functions are documentated in one location. 
Registration is optional, dependent on the passed arguments
"signal_key" and "update_key". 

To use widget library, there are three use cases. 
1) Init the widget and provide informative identifiers for signal_key and update_key.
   The controller will access the signal and update maps with these keys.
2) Init the widget without signal and update keys as part of a composite widget.
   In this case, the widget's signal does not correspond to core application logic, 
   but is useful in orchestrating a composite widget. Thus, the widget's signal
   should not registered in signal map.
3) Init the widget without signal and update keys to display as a static widget.
   Good examples are images or labels. 

To implement a new widget, define two things:
1) Widget Defaults.
2) Support for registering signals / update functions. """

""" --- Widget Primitives --- """
class HSeperationLine(QFrame):
  def __init__(self):
    super().__init__()
    self.setFixedHeight(20)
    self.setFrameShape(QFrame.HLine)
    self.setFrameShadow(QFrame.Sunken)
    self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

class Heading(QLabel):
  def __init__(self, text, font_size):
    super().__init__()
    self.setText(text)
    self.setFont(QFont('Roboto', font_size))
    
class TextBox(QLabel):
  def __init__(self, label_string, font_size=8, wordWrap=True, update_key=None):
    super().__init__()
    self.setText(label_string)
    self.setFont(QFont('Roboto', font_size))
    self.setWordWrap(wordWrap)
    if update_key is not None:
      view_api.add_to_update_map(self.updateTextBox, update_key)

  def updateTextBox(self, label_string):
    self.setText(label_string)

class Button(QPushButton):
  def __init__(self, signal_key=None, update_key=None):
    super().__init__()
    if signal_key is not None:
      view_api.add_to_signal_map(self.clicked, signal_key)
    if update_key is not None:
      view_api.add_to_update_map({"disable": self.disable, "enable": self.enable}, update_key)

  def disable(self):
    self.setEnabled(False)

  def enable(self):
    self.setEnabled(True)

class LineEditLayout(QFormLayout):
  def __init__(self, label_text, edit_text, font_size=8, signal_key=None, update_key=None):
    super().__init__()
    self.line_edit = QLineEdit(edit_text)
    self.line_edit.setFont(QFont("Roboto", font_size))
    self.addRow(label_text, self.line_edit)
    if signal_key is not None:
      view_api.add_to_signal_map(self.line_edit.textChanged, signal_key)
    if update_key is not None:
      view_api.add_to_update_map(self.updateEditText, update_key)
  
  def updateEditText(self, update_string):
    self.line_edit.setText(update_string)

class ListWidget(QListWidget):
  def __init__(self, signal_key=None, update_key=None):
    super().__init__()
    if signal_key is not None:
      view_api.add_to_signal_map(self.itemActivated, signal_key)
    if update_key is not None:
      view_api.add_to_update_map(self.updateListWidget, update_key)

  def getCurrentRow(self):
    return self.currentRow()
  
  def getCurrentText(self):
    return self.currentItem().text()

  def updateListWidget(self, string_list):
    self.clear()
    for string in string_list:
      self.addItem(string)

class Spacer(QSpacerItem):
  def __init__(self, width=20, height=70):
    super().__init__(width, height, QSizePolicy.Preferred, QSizePolicy.Preferred)

class Slider(QSlider):
  index = pyqtSignal(int)

  def __init__(self, parent, min, max, signal_key=None, update_key=None):
    super().__init__(parent)
    self.setOrientation(Qt.Horizontal)
    self.setRange(min, max)
    if signal_key is not None:
      # Send index on value change 
      self.valueChanged.connect(lambda: self.index.emit(self.value()))
      view_api.add_to_signal_map(self.index, signal_key)
    if update_key is not None:
      view_api.add_to_update_map(self.updateSliderLength, update_key)
    
  def updateSliderLength(self, length):
    self.setMaximum(length)

class Image(QLabel):
  def __init__(self, image_path, update_key=None):
    super().__init__()
    pixmap = QPixmap(image_path)
    self.setPixmap(pixmap)
    if update_key is not None:
      view_api.add_to_update_map(self.updateImage, update_key)

  def updateImage(self, image_path):
    pixmap = QPixmap(image_path)
    self.setPixmap(pixmap)

class Dialog(QDialog): #Replace with QFrame
  def __init__(self, window_title): # Add a Close Signal
    super().__init__()
    self.setWindowTitle(window_title)
    # Close on close signal (typically the main window)
    # close_signal.connect(lambda: self.close())

  def run_dialog(self):
    self.exec_()  # Replace with .show()

""" --- Widget Composites --- """
class UploadWidget(QFrame):
  # Define unique UploadWidget signal that emits the retrieved path string
  pathstring = pyqtSignal(str)

  def __init__(self, signal_key, update_key=None):
    super().__init__()
    # Button / Label Pairing
    self.button = QPushButton()
    self.button.setIcon(QIcon(":upload-icon"))
    self.button.setIconSize(QSize(50, 50))
    # self.button.setStyleSheet("background-color: silver")
    self.directory_label = TextBox("")

    #Layout
    layout = QVBoxLayout()
    layout.addWidget(self.button)
    layout.addWidget(self.directory_label)
    self.setLayout(layout)

    # Internal control logic to UploadWidget which triggers QFileDialog automatically
    self.button.clicked.connect(self._open)

    # Register Custom Signal
    view_api.add_to_signal_map(self.pathstring, signal_key)
    # Register Update Function
    if update_key is not None:
      view_api.add_to_update_map(self.updateDirectoryLabel, update_key)

  def _open(self):
    dirname = QFileDialog.getExistingDirectory(self, 'Open Directory')
    if dirname:
      self.directory_label.setText(f"Uploaded Directory: {Path(dirname).name}")
      self.pathstring.emit(str(dirname))

  def updateDirectoryLabel(self, dirname):
    self.directory_label.setText(f"Uploaded Directory: {Path(dirname).name}")

class Selector(QFrame):
  # Define unique Selector signal that emits the user's selection
  selection = pyqtSignal(str)

  def __init__(self, widget_map=None, signal_key=None):
    super().__init__()
    # Combobox / Stacked Widget Pairing
    self.combobox = QComboBox()
    self.stack = QStackedWidget()

    # Init widget map
    self.widget_map = {}
    # Fill map if widget map provided 
    if widget_map is not None:
      for name, widget in widget_map.items():
        self.combobox.addItem(name)
        self.stack.addWidget(widget)
      self.widget_map = widget_map

    # Layout
    layout = QVBoxLayout()
    layout.addWidget(self.combobox)
    layout.addWidget(self.stack)
    self.setLayout(layout)

    # Internal control logic to Selector for automatic widget navigation
    self.combobox.activated.connect(self._navigate)
    
    # Register Custom Signal
    if signal_key is not None:
      view_api.add_to_signal_map(self.selection, signal_key)

  def _navigate(self):
    self.stack.setCurrentIndex(self.combobox.currentIndex())
    self.selection.emit(str(self.combobox.currentText()))
  
  def addSelection(self, name, widget):
    self.widget_map[name] = widget
    self.combobox.addItem(name)
    self.stack.addWidget(widget)

  def getCurrentSelection(self):
    return self.combobox.currentText()

  def getCurrentWidget(self):
    return self.widget_map[self.combobox.currentText()]

class ListWidgetSelector(QFrame):
  selection = pyqtSignal(tuple) #2-ple: (name, index)
  renamedFile = pyqtSignal(tuple) # 3-ple: (name, index, updated_name)
  deletion = pyqtSignal(tuple) #3-ple: (name, index, deleted_name)

  def __init__(self, select_names, signal_key=None, update_key=None):
    super().__init__()
    # Init a blank Selector
    self.selector = Selector()
    self.widget_map = self.selector.widget_map

    # Customize Selector
    for name in select_names:
      self.selector.addSelection(name, ListWidget())

    for _, list_widget in self.widget_map.items(): 
      # Connect ListWidget Signals to unifed callback 
      list_widget.itemClicked.connect(self._listItemSelected)

      # Define Popup Menus for List Widgets
      list_widget.setContextMenuPolicy(Qt.ActionsContextMenu)
      self.deleteAction = QAction(self)
      self.deleteAction.setText("Delete")
      list_widget.addAction(self.deleteAction)

      # Connect List Widget Edit / Popup Signals to Unified Callback
      list_widget.itemChanged.connect(self._renameFile)
      self.deleteAction.triggered.connect(self._deleteFile)

    # Layout
    layout = QVBoxLayout()
    layout.addWidget(self.selector)
    self.setLayout(layout)

    # Register Custom Signal
    if signal_key is not None:
      view_api.add_to_signal_map(self.selection, signal_key=signal_key) 
      view_api.add_to_signal_map(self.renamedFile, signal_key=signal_key+"_rename")
      view_api.add_to_signal_map(self.deletion, signal_key=signal_key+"_deletion")

    # Register Update Function 
    if update_key is not None:
      view_api.add_to_update_map(self.updateWeights, update_key=update_key)

  def _listItemSelected(self):
    # Emit Signal 
    selection = self.getCurrentSelection()  
    list_widget = self.getCurrentWidget()
    index = list_widget.getCurrentRow()
    self.selection.emit((selection, index))
    # print("Item Selected Signal:", selection, index)

  def _renameFile(self, changedItem):
    # Emit Signal 
    selection = self.getCurrentSelection()
    list_widget = self.getCurrentWidget()
    index = list_widget.getCurrentRow()
    text = changedItem.text()
    self.renamedFile.emit((selection, index, text))
    # print("Rename signal:", selection, index, text)

  def _deleteFile(self):
    # Emit Signal 
    selection = self.getCurrentSelection()
    list_widget = self.getCurrentWidget()
    if list_widget.currentItem() is not None:
      deleted_name = list_widget.getCurrentText()
      index = list_widget.getCurrentRow()
      list_widget.takeItem(index)
      self.deletion.emit((selection, index, deleted_name))
      # print("Delete signal:", selection, index, deleted_name)

  def getCurrentSelection(self):
    return self.selector.getCurrentSelection()

  def getCurrentWidget(self):
    return self.selector.getCurrentWidget() 

  def updateWeights(self, selection, entries):
    # Update selection's List Widget with provided entries
    list_widget = self.widget_map[selection]
    list_widget.updateListWidget(entries)

    # Make List Widget Items Editable for Renaming
    for index in range(list_widget.count()):
      item = list_widget.item(index)
      item.setFlags(item.flags() | Qt.ItemIsEditable)

  def addSelection(self, name, list_widget):
    # Add the name-widget pairing to the map
    self.widget_map[name] = list_widget

    # Make List Widget Items Editable
    for index in range(list_widget.count()):
      item = list_widget.item(index)
      item.setFlags(item.flags() | Qt.ItemIsEditable)

    # Connect the widget to the selector callback
    list_widget.itemClicked.connect(self._listItemSelected)

    # Connect to other callbacks as well 
    list_widget.setContextMenuPolicy(Qt.ActionsContextMenu)
    self.deleteAction = QAction(self)
    self.deleteAction.setText("Delete")
    list_widget.addAction(self.deleteAction)
    
    list_widget.itemChanged.connect(self._renameFile)
    self.deleteAction.triggered.connect(self._deleteFile)