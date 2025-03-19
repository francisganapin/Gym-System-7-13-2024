#################################third party import
from PyQt6.QtWidgets import  QDialog
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog

#################################



class CustomConfirmDialog(QDialog):
    '''WE USE THIS IF Confirmation for delete member admin
    '''
    def __init__(self, member_id, member_name, parent=None):
        super().__init__(parent)
        uic.loadUi('delete.ui', self)

        # Set fixed size to prevent resizing
        self.setFixedSize(self.size())
        # Update the label to include ID and name

        self.label_for_delete.setText(f'Are you sure you want to delete this member : {member_id}')
        self.label_for_delete_2.setText(f'with member name of? {member_name}')
        # Connect buttons to dialog slots
        self.yes_button_2.clicked.connect(self.accept)
        self.no_button.clicked.connect(self.reject)

    def exec_dialog(self):
        return self.exec()