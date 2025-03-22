import sys
import os
import sqlite3
from PyQt6.QtCore import QTimer
#################################third party import
from PyQt6.QtWidgets import  QDialog, QLineEdit
from PyQt6 import uic
from PyQt6.QtWidgets import QDialog

#################################





class LoginDialog(QDialog):
    '''Display data and this was the framework of our app before they can login'''
    def __init__(self):
        super().__init__()
        
        #connect to other folder in other folder 
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ui', 'login.ui')
        
        # Load the UI file
        uic.loadUi(ui_path, self)

        # Set fixed size to prevent resizing
        self.setFixedSize(self.size())
        self.username_input.text()
        self.password_input.text()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button.clicked.connect(self.check_credentials)


    def check_credentials(self):
        '''Check the credentials of the user'''
        self.username = self.username_input.text()
        password = self.password_input.text()

        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'database.db')
    
        with sqlite3.connect(file_path) as conn:
            self.cursor = conn.cursor()

            query = 'SELECT * FROM users WHERE username = ? AND password = ?'

            self.cursor.execute(query, (self.username, password))
            result = self.cursor.fetchone()

            if result:
                self.accept()
            else:
                self.username_input.text()
                self.password_input.text()
                # Pop up invalid credentials
                self.invalid_label.setText('Invalid Credentials')
                QTimer.singleShot(3000, lambda: self.invalid_label.setText(''))

    
    def exec_dialog(self):
        """Executes the dialog and returns the result."""

        result = self.exec()
        if result == QDialog.Rejected:
            sys.exit()



    def clear_credentials(self):
        '''clear the input method'''
        self.username_input.clear()
        self.password_input.clear()
        self.username_input.setFocus()


    def closeEvent(self,event):
        event.accept()
        sys.exit()
