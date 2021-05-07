# ---- External Lib Imports ----
from PyQt5.QtWidgets import(
  QFrame, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
)
# ---- Local Lib Imports ----
from app.view.widgets import (HSeperationLine, LineEditLayout, Button, TextBox, 
  UploadWidget, Selector, Heading, Spacer 
)
import app.view.api as view_api

""" --- Custom Data Prep Panel Widgets --- """



""" --- Data Prep Panel Widget --- """
class DataPrepView(QFrame):
  def __init__(self):
    super().__init__()

    # Build Custom Widgets:
    layout = QVBoxLayout()
    layout.addWidget(Heading(' Data Preparation', font_size=20))
    layout.addWidget(HSeperationLine())
    layout.addItem(QSpacerItem(20, 150, QSizePolicy.Preferred, QSizePolicy.Expanding))
    self.setLayout(layout)