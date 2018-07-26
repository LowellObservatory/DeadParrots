'''
Created on Jul 10, 2018

@author: dlytle
'''

import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QMessageBox, QVBoxLayout,
                             QMainWindow)
from PyQt5 import QtCore

from FileList import FileList
from ImageDisplayWindow import StaticImageDisplayWindow

class ApplicationWindow(QMainWindow):
    """ The main window of this GUI."""
    
    def __init__(self):
        """ Create the main window, add the file list and the image display
            widgets."""
            
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("FITSBrowse")

        self.main_widget = QWidget(self)

        layout = QVBoxLayout(self.main_widget)
        
        # Default size of the image display is 800x800 and axes are displayed.
        image_display_figure = StaticImageDisplayWindow(self.main_widget,
                                                        width=8, height=8,
                                                        dpi=100)
        file_list = FileList(image_display_figure)

        # The layout has the list widget above the image display widget.
        layout.addWidget(file_list)
        layout.addWidget(image_display_figure)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)


    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()
        
    def about(self):
        QMessageBox.about(self, "About", """FITSBrowse""")


if __name__ == '__main__':
    
    # Run the program.
    app = QApplication(sys.argv)
    
    ex = ApplicationWindow()
    ex.show()
    sys.exit(app.exec_())
    