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
# 1) Develop Logger, modifying the weights/logs will modify the other.
# This is easily achieved by routing the signals to one another.

# 2) Develop Explorer
# - Enlarge Inference Images 

# 2a) Cache on Image Directory AND Checkpoint path. B/c results is data + code! 
# 2b) Make child windows, the extra windows are annoying :P
# How? Try creating a separate view ui map for holding ref to windows. 
# On a main window close event, set these references to null/do any application pickling business. 

# Also, create close events/custom close signals for Dialog widget.
# This way, we can disable/enaable buttons depending if corresponding window is open or not for idemponcy. 

# --------------------------------
# 3) Make Object Detection Model

# 4) Make Dakota's Panel 