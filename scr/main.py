import sys
import os
from PyQt5 import QtWidgets


sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from ui_functions.launch_screen_function import LaunchScreen



# Index for which screen: 
# 0 : launch screen

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.stackedWidget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stackedWidget)


        # initialize all of the screens 
        self.launch_screen = LaunchScreen(self)

        # This adds the screens to the stack. The index is how you know what screen to switch to
        # add the screen to the stack                       # Index 
        self.stackedWidget.addWidget(self.launch_screen)    # 0

        
        # initializing to the launch screen 
        self.stackedWidget.setCurrentIndex(0)

        self.resize(1024,600) # setting the size of the screen 
        self.setMaximumSize(1024,600)

        self.move(0,0)
        
    def setIndex(self, index):
        self.stackedWidget.setCurrentIndex(int(index))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())