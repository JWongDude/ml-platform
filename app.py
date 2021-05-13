# ----- app.py -----
# Application Startup

import sys
from PyQt5.QtWidgets import QApplication
import app.view.ui as ui
import app.controller as controller

# Temp main function 
def main():
    # Init Event Loop 
    app = QApplication([])
    app.setStyle('Breeze')
    
    # Init View
    view = ui.PlatformUi()

    # Pass Model and View Configurations
    # controller.loadApplication()

    # Init Controller
    controller.recoverApplicationState()
    controller.connectMainWindowSignals()
    controller.connectDialogSignals()
    
    # Run PyQt Event Loop
    view.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

# TODO:
# Weekend Freetime: 
# Make Dakota's Panel -- should be 30 min - 1hr

# --------------------------------
# 3) Make Object Detection Model
# 3a) Checkout CVAT for their output formats
# 3b) Work with CVAT outputs, change Image Classification to work with simple image directory.
# 3c) Figure out *what* to log and *what* predictions to pass on to inference panel
# I anticipate visualizing bounding boxes / segmentation masks might be unique custom work