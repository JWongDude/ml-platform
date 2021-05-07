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


# Def make logging view so that user is able to delete logs.
# Is it a good idea to delete logs and weight together? Yes.
# Is it a good idea to delete from two places? Yes. 
# It's not bad at all. Make 

# TODO:
# 1) Develop Logger, modifying the weights/logs will modify the other.
# This is easily achieved by routing the signals to one another.

# 1a) Move the logs/weights to artifacts folder, I have more confidence I can figure out relative imports

# 2) Develop Explorer
# - Enlarge Inference Images 

# --------------------------------
# 3) Make Object Detection Model

# 4) Make Dakota's Panel 