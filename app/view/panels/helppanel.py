# ---- External Lib Imports ----
# Utility Widgets
from PyQt5.QtWidgets import(
  QFileDialog, QComboBox, QLineEdit, QPushButton, QLabel, QAction)

# Organization Widgets
from PyQt5.QtWidgets import(
  QFrame, QSpacerItem, QSizePolicy, QVBoxLayout, QFormLayout)
from PyQt5.QtCore import (Qt, QSize)

# Style Widgets
from PyQt5.QtGui import (QIcon, QFont)

# ---- Local Lib Imports ----
import view.widgets as widgets

class HelpView(QFrame):
  def __init__(self):
    super().__init__()
    pass