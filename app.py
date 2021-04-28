# ----- app.py -----
# Application Startup

import sys
from PyQt5.QtWidgets import QApplication
import view.ui as ui
import controller

# Temp main function 
def main():
    # Spinup Application 
    app = QApplication([])
    app.setStyle('Breeze')

    # Build Application
    view = ui.PlatformUi()

    # control.loadApplication()
    controller.recoverApplicationState()
    controller.connectMainWindowSignals()
    controller.connectDialogSignals()

    # Run PyQt Event Loop
    view.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()