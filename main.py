import sys
from datetime import datetime
import os
import sqlite3
import csv

from PyQt6 import QtWidgets,uic
from PyQt6.QtCore import QTimer
from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import (
    QApplication, QDialog, QLineEdit, QMessageBox, QVBoxLayout,
    QStackedWidget, QWidget, QFileDialog, QLabel, QPushButton
)

# our module
from module.dis_member_login import LoginMemberDisplay  # m1
from module.insert_data import InsertValue  # m2
from module.show_database import ShowDatabaseDisplay  # m3
from module.manager import ManagerModule #m4
from module.confirm_dialog import CustomConfirmDialog
from module.login import LoginDialog




class MyApp(QtWidgets.QWidget):
    ''' display oru data so that it would work
    '''
    def __init__(self,username=None):
        super().__init__()
        uic.loadUi('ui/gym.ui', self)
       
        # Set fixed size to prevent resizing
        self.setFixedSize(self.size())

        # Store the username
        self.username = username


        # initialize save path
        self.save_path = None

        # Apply the dark theme


        self.model_2 = QStandardItemModel()
        self.model_2.setHorizontalHeaderLabels(["Id","Name",'Membership',"Email", "Expiry_date", "Contact", "Gender", "Birthday", "Address","Image"])
        self.tableView_2.setModel(self.model_2)
        
        self.model_4 = QStandardItemModel()
        self.model_4.setHorizontalHeaderLabels(["Id","Name",'Membership',"Email", "Expiry_date", "Contact", "Gender","Birthday", "Address","Image"])
        self.tableView_4.setModel(self.model_4)

        # Load the data when the application starts
        
    
        #module
       

        self.m1 = LoginMemberDisplay(self)
        self.Login_bt.clicked.connect(self.m1.display_member_data)

        self.m2 = InsertValue(self)  
        self.register_button.clicked.connect(self.m2.insert_data)
        self.upload_button_2.clicked.connect(self.m2.upload_image)

        self.m3 = ShowDatabaseDisplay(self)
        self.model_1 = QStandardItemModel()
        self.model_1.setHorizontalHeaderLabels(["Id", "Name", "Membership", "Email", "Expiry_date", "Contact", "Gender", "Birthday", "Address", "Image"])

        self.tableView_3_model = QStandardItemModel()

        if self.m3.ui.tableView:
            self.m3.ui.tableView.setModel(self.model_1)

        self.SearchButton.clicked.connect(self.m3.search_data)
        self.Save_Date_Bt.clicked.connect(self.m3.edit_item)
       
        self.m3.show_database()
      
        self.Save_Date_Bt.clicked.connect(self.m3.edit_item)
        

        #this is m4 module
        self.m4 = ManagerModule(self)

        self.login_button_2.clicked.connect(self.m4.check_credentials_manager)
        self.search_bt_manager.clicked.connect(self.m4.search_data_manger)
        self.delete_bt_manager_2.clicked.connect(self.m4.delete_selected_row)
        self.back_bt_manager.clicked.connect(self.m4.back_manager_page)
    
        self.m4.delete_database_manager()

        self.m4.delete_database_manager()

        if self.m4.ui.tableView:
            self.m4.ui.tableView.setModel(self.model_4)

        ###############################################################
       
        ###############################################################

        # Load login records initially
        # Set up the timer to update the time every second
        
        ########################## display all login record in page  Login Data Page
        self.display_login_records()

        # show date  and time 

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000) ## update every seconds

        ################## Show the current login user 
        self.label_username()


        ##### this would we should add this so our  display fucntion would work
       
       

       # Access the stacked widget and the pages
        self.stackedWidget = self.findChild(QStackedWidget, 'stackedWidget')
        self.page_1 = self.findChild(QWidget, 'page_1')
        self.page_2 = self.findChild(QWidget, 'page_2')
        self.password_input_2.setEchoMode(QLineEdit.EchoMode.Password)

        # We use this folder to save the image we upload 
        self.save_folder ='Image'
        os.makedirs(self.save_folder,exist_ok=True)

        # Access widgets by their names in the .ui file
        self.image_label_2 = self.findChild(QLabel, "image_label_2")
        self.upload_button_2 = self.findChild(QPushButton, "upload_button_2")

        # Debug: Check if widgets are loaded correctly
        if self.image_label_2 is None:
            raise ValueError("Widget 'image_label_2' not found. Check the .ui file.")
        if self.upload_button_2 is None:
            raise ValueError("Widget 'upload_button' not found. Check the .ui file.")

                     #set max lenght for selected input
        if self.id_input:
            self.id_input.setMaxLength(10)
        if self.contact_input:
            self.contact_input.setMaxLength(11)
        if self.id_search_input:
            self.id_search_input.setMaxLength(10)
        if self.id_entry:
            self.id_entry.setMaxLength(10)
 
        


    

    def display_login_records(self):
        """
        Display login records from login_records.csv in a PyQt TableView.
        """
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'login_records.csv')

        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                data = list(reader)

            # Initialize a new model if it doesn't exist
            if not hasattr(self, 'tableView_3_model'):
                self.tableView_3_model = QStandardItemModel()

            # Set headers
            if data:
                self.tableView_3_model.setHorizontalHeaderLabels(data[0])

            # Populate data rows
            for row in data[1:]:
                items = [QStandardItem(field) for field in row]
                self.tableView_3_model.appendRow(items)

            print('Login Records Displayed Successfully')

            # Ensure tableView_3 updates with the new model
            self.tableView_3.setModel(self.tableView_3_model)
            self.tableView_3.repaint()  # Or self.tableView_3.update()

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except IOError as e:
            print(f"Error reading file '{file_path}': {e}")
        except csv.Error as e:
            print(f"CSV error while reading file '{file_path}': {e}")
        except Exception as e:
            print(f"Unexpected error displaying login records: {e}")

    def show_frame(self):
        """
            this one if you finish the login and authenticate it will show the frame
        """
        self.Frame.show()

    def update_time(self):

        now = datetime.now()
   
        dt_string = now.strftime("%A | %B | %d | %y %I:%M %p")

        self.date_label.setText(dt_string)

    def label_username(self):
        '''Label username from the database'''
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'database.db')
        
        with sqlite3.connect(file_path) as conn:
            self.cursor = conn.cursor()
            query = 'SELECT username FROM users WHERE username = ?'
            self.cursor.execute(query, (self.username,))
            result = self.cursor.fetchone()
            if result:
                username = result[0]
                self.username_label.setText(f'Hi {username}')

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    if login_dialog.exec() == QDialog.DialogCode.Accepted:
        main_app = MyApp(username=login_dialog.username)  # Pass the username
        main_app.show()
        main_app.show_frame()  # Show the frame only after successful authentication

    sys.exit(app.exec())