# ----- app.py -----
# Application Startup

import sys
from PyQt5.QtWidgets import QApplication
import app.view.ui as ui
import app.controller as controller
import app.view.api as view_api

# Temp main function 
def main():
    # Init Event Loop 
    app = QApplication([])
    app.setStyle('Breeze')
    view_api.add_to_signal_map(app.aboutToQuit, "close_signal")

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
# Do the other quality of life: 
# - Make Dakota's Panel 
# - Tensorboard Subprocess, modifying the weights/logs will modify the other.
# This is easily achieved by routing the signals to one another.

# - Enlarge Inference Images 
# - Register Main Window Close signal and rig to close Tensorboard thread and Inference Window. 