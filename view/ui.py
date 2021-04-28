# ---- Standard Lib Imports ----
from functools import partial 

# ---- External Lib Imports ----
# Main Window Widgets
from PyQt5.QtWidgets import(
  QMainWindow, QStackedWidget, QToolBar, QAction)
from PyQt5.QtCore import (Qt, QSize)
from PyQt5.QtGui import (QIcon)

# ---- Local Lib Imports ----
import view.icon_resources
from view.panels.modelpanel import ModelView
from view.panels.inferencepanel import InferenceView
from view.panels.helppanel import HelpView

class PlatformUi(QMainWindow):
  def __init__(self):
    super().__init__()
  
    # Initialize Application View
    self.setWindowTitle('Boeing Computer Vision Platform')
    self.setFixedSize(800, 900)
    self.Stack = QStackedWidget(self)
    self.panel1 = ModelView()
    self.panel2 = InferenceView()
    self.panel3 = HelpView()
    self.Stack.addWidget(self.panel1) 
    self.Stack.addWidget(self.panel2)
    self.Stack.addWidget(self.panel3)
    self.setCentralWidget(self.Stack)

    # Setup Application Navigation
    self._createNavigationBar()

  def _createNavigationBar(self):
    # Load in button icons
    self.trainButton = QAction(QIcon(":train-icon"), "Train", self)
    self.scoreButton = QAction(QIcon(":score-icon"), "Score", self)
    self.launchButton = QAction(QIcon(":magnify-icon"), "Inference", self)

    # Create toolbar, add icons
    navigationBar = QToolBar("Navigation", self)
    navigationBar.addAction(self.trainButton)
    navigationBar.addAction(self.scoreButton)
    navigationBar.addAction(self.launchButton)
    navigationBar.setIconSize(QSize(75, 75))
    navigationBar.setMovable(False)

    # TODO: Move to a dedicated style sheet 
    navigationBar.setStyleSheet("background-color: #3895d3")

    self.addToolBar(Qt.LeftToolBarArea, navigationBar)
    
    # Define page navigation
    self.trainButton.triggered.connect(partial(lambda x: self.Stack.setCurrentIndex(x), 0)) 
    self.scoreButton.triggered.connect(partial(lambda x: self.Stack.setCurrentIndex(x), 1))
    self.launchButton.triggered.connect(partial(lambda x: self.Stack.setCurrentIndex(x), 2))