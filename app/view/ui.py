# ---- Standard Lib Imports ----
from functools import partial 

# ---- External Lib Imports ----
# Main Window Widgets
from PyQt5.QtWidgets import(
  QMainWindow, QStackedWidget, QToolBar, QAction, QSizePolicy)
from PyQt5.QtCore import (Qt, QSize)
from PyQt5.QtGui import (QIcon)

# ---- Local Lib Imports ----
import app.view.icon_resources
from app.view.panels.modelpanel import ModelView
from app.view.panels.inferencepanel import InferenceView
from app.view.panels.datapreppanel import DataPrepView

class PlatformUi(QMainWindow):
  def __init__(self):
    super().__init__()
  
    # Initialize Application View
    self.setWindowTitle('Boeing Computer Vision Platform')
    self.Stack = QStackedWidget(self)
    self.panel1 = DataPrepView()
    self.panel2 = ModelView()
    self.panel3 = InferenceView()
    self.Stack.addWidget(self.panel1) 
    self.Stack.addWidget(self.panel2)
    self.Stack.addWidget(self.panel3)
    self.setCentralWidget(self.Stack)

    # Setup Application Navigation
    self._createNavigationBar()

    # Setup Resizable Window
    sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    self.setSizePolicy(sizePolicy)

  def _createNavigationBar(self):
    # Load in button icons
    self.data_prep_button = QAction(QIcon(":image-icon"), "Data Preparation", self)
    self.train_button = QAction(QIcon(":train-icon"), "Model Training", self)
    self.predict_button = QAction(QIcon(":magnify-icon"), "Model Prediction", self)

    # Create toolbar, add icons
    navigationBar = QToolBar("Navigation", self)
    navigationBar.addAction(self.data_prep_button)
    navigationBar.addAction(self.train_button)
    navigationBar.addAction(self.predict_button)
    navigationBar.setIconSize(QSize(75, 75))
    navigationBar.setMovable(False)

    # Style
    navigationBar.setStyleSheet("background-color: #3895d3")
    self.addToolBar(Qt.LeftToolBarArea, navigationBar)
    
    # Define page navigation
    self.data_prep_button.triggered.connect(partial(lambda x: self.Stack.setCurrentIndex(x), 0))
    self.train_button.triggered.connect(partial(lambda x: self.Stack.setCurrentIndex(x), 1)) 
    self.predict_button.triggered.connect(partial(lambda x: self.Stack.setCurrentIndex(x), 2))