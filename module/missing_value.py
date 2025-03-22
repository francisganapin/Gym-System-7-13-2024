#################################third party import
from PyQt6.QtWidgets import  QDialog
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog
import os
#################################

class MissingValueDialog(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)

             
        #connect to other folder in other folder 
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ui', 'missing_value.ui')
        
        # Load the UI file
        uic.loadUi(ui_path, self)
    
        self.setWindowTitle('Missing Value')
        # Set fixed size to prevent resizing
        self.setFixedSize(self.size())
        # Update the label to include ID and name

        self.label_for_delete.setText(message)

    def exec_dialog(self):
        return self.exec()
