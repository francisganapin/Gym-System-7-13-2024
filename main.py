import sys
from datetime import datetime
import os
import sqlite3
import csv
from PIL import Image
from PyQt6.QtCore import QTimer
from PyQt6 import QtCore
from PyQt6.QtGui import QPixmap 
#################################third party import
from PyQt6.QtWidgets import QApplication, QDialog, QLineEdit
from PyQt6 import QtWidgets,uic
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QDialog,QVBoxLayout
from PyQt6.QtWidgets import QApplication,QStackedWidget, QWidget,QFileDialog
#################################
from PyQt6.QtWidgets import QApplication, QFileDialog, QLabel, QPushButton
from PyQt6.QtCore import QDate
# our module
from module.dis_member_login import LoginMemberDisplay
from module.confirm_dialog import CustomConfirmDialog
from module.login import LoginDialog
from module.show_database import ShowDatabaseDisplay
from module.insert_data import InsertValue

class MyApp(QtWidgets.QWidget):
    ''' display oru data so that it would work
    '''
    def __init__(self,username=None):
        super().__init__()
        uic.loadUi('gym.ui', self)
       
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
        
        self.delete_database_manager()

        #module
       

        self.m1 = LoginMemberDisplay(self)
        self.Login_bt.clicked.connect(self.m1.display_member_data)

        self.wew = InsertValue(self)  
        self.register_button.clicked.connect(self.wew.insert_data)
        self.upload_button_2.clicked.connect(self.wew.upload_image)

        self.m3 = ShowDatabaseDisplay(self)
        self.model_1 = QStandardItemModel()
        self.model_1.setHorizontalHeaderLabels(["Id", "Name", "Membership", "Email", "Expiry_date", "Contact", "Gender", "Birthday", "Address", "Image"])

  
        if self.m3.ui.tableView:
            self.m3.ui.tableView.setModel(self.model_1)

        self.SearchButton.clicked.connect(self.m3.search_data)
        self.Save_Date_Bt.clicked.connect(self.m3.edit_item)
       
        self.m3.show_database()












  
      
        self.Save_Date_Bt.clicked.connect(self.m3.edit_item)
        
        self.login_button_2.clicked.connect(self.check_credentials_manager)
        self.search_bt_manager.clicked.connect(self.search_data_manger)
        self.delete_bt_manager_2.clicked.connect(self.delete_selected_row)
        self.back_bt_manager.clicked.connect(self.back_manager_page)
       
        
        self.tableView_3_model = QStandardItemModel()


        ###############################################################
       
        ###############################################################

        # Load login records initially
        # Set up the timer to update the time every second
        
        ########################## display all login record in page  Login Data Page
        self.display_login_records()
        self.delete_database_manager()
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
 
        


    def delete_database_manager(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'members.db')
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT Id, Name, Membership,Email, Expiry_date, Contact, Gender, Birthday, Address, Image FROM members")
            rows = cursor.fetchall()

            self.model_4.removeRows(0, self.model_4.rowCount())  # Clear the model

            for row_data in rows:
                items = [QStandardItem(str(data)) for data in row_data]
                self.model_4.appendRow(items)

            print('Data Fetched Successfully')
        except sqlite3.Error as e:
            print(f'Sqlite error: {e}')
        finally:
            conn.close()

    

    def edit_item(self):
        '''this one is edit for data on selected member 
            in order to update the data it should specify the 
            target member

            this one is connected to model_2
        '''
        
        selected_index = self.tableView_2.selectionModel().currentIndex()
        selected_row = selected_index.row()
        # Check if a valid row is selected
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "No row is selected.")
            return
        item_id = self.model_2.item(selected_row, 0).text()
        # Check if item_id is valid (not empty)
        if not item_id:
            QMessageBox.warning(self, "Selection Error", "No item is selected.")
            return
        new_expiry = self.Expiry_edit.selectedDate().toString("yyyy-MM-dd")
        # Update the model in the table view
        self.model_2.setItem(selected_row,3,QStandardItem(new_expiry))  # Assuming column 3 is Expiry
        # Update the database
        current_directory = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_directory, 'members.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE members
                SET Expiry_date = ?
                WHERE Id = ?
            ''', (new_expiry, item_id))
            conn.commit()
            print('Data Updated Successfully')
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            conn.close()
        #main.py:215:0: C0301: Line too long (101/100) (line-too-long)



    def display_member_data(self):
        """display them if they are in login so that the 
        employee will know  if they are expired """
        member_id = self.id_entry.text()
    
        member = self.fetch_data_member(member_id)
        
        if member:
            self.name_label.setText(f"Name: {member[0]}")
        
            expiry_date_str = member[1]

            image_member = member[2]

            expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
            current_date = datetime.now().date()
            
            pixmap = QPixmap(image_member)
            self.image_label.setPixmap(pixmap)

            if not os.path.exists(image_member):
                self.image_label.setText('image does not exist')
                
            
            self.expiry_label.setText(f"Expiry: {expiry_date_str}")
            print(image_member)

            
            if expiry_date < current_date:

                self.expiry_label.setStyleSheet("color: red; font: 900 italic 18pt")
            else:
                self.expiry_label.setStyleSheet("color: green; font: 900 italic 18pt")  # Reset to default color
          
            
            self.save_login_record(member[0])
            QTimer.singleShot(3000, lambda: self.image_label.clear())
            QTimer.singleShot(3000, lambda: self.name_label.clear())
            QTimer.singleShot(3000, lambda: self.expiry_label.clear())
        else:
            QMessageBox.information(self, "Not Found", "Member not found.")

    def save_login_record(self, member_name):
        """
        this code if the person was login it would save at login_records.csv
        """
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record = [member_name, current_time,self.username]

            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, 'login_records.csv')

            file_exists = os.path.isfile(file_path)
            with open(file_path, 'a', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Name", "Login Time",'Employee'])
                writer.writerow(record)
            print("Record saved successfully.")
        except FileNotFoundError :
            print(f"Error: File '{file_path}' not found.")
        except IOError as e:
            print(f"Error writing to file '{file_path}': {e}")
        except Exception as e:
            print(f"Unexpected error saving record: {e}")
    
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

    def check_credentials_manager(self):
        '''Check the credentials of the user'''
        self.manger = self.username_input_2.text()
        password = self.password_input_2.text()
        self.password_input_2.setEchoMode(QLineEdit.EchoMode.Password)

        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'database.db')
    
        with sqlite3.connect(file_path) as conn:
            self.cursor = conn.cursor()

            query = 'SELECT * FROM users WHERE username = ? AND password = ?'

            self.cursor.execute(query, (self.username, password))
            result = self.cursor.fetchone()

            if result:
                self.stackedWidget.setCurrentWidget(self.page_2)
            else:
                self.username_input_2.text()
                self.password_input_2.text()
                # Pop up invalid credentials
                self.invalid_label_2_manger.setText('Invalid Credentials')
                QTimer.singleShot(3000, lambda: self.invalid_label_2_manger.setText(''))

    def clear_credentials_manager(self):
        '''clear the input method'''
        self.username_input_2.clear()
        self.username_input_2.clear()
        self.username_input_2.setFocus()

    def search_data_manger(self):
        """
        Search the data in the second tab. 
        You can choose to search by name or ID.
        """
        search_name_manger = self.name_search_manger_input.text()
        search_id_manger = self.id_search_manager_input.text()
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'members.db')
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        query = "SELECT Id, Name, Email, Membership,Expiry_date, Contact, Gender, Birthday, Address FROM members WHERE 1=1"
        params = []

        if search_name_manger:
            query += " AND Name LIKE ?"
            params.append(f"%{search_name_manger}%")

        if search_id_manger:
            query += " AND Id = ?"
            params.append(search_id_manger)

        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()

            self.model_4.removeRows(0, self.model_4.rowCount())  # Clear the model

            for row_data in rows:
                items = [QStandardItem(str(data)) for data in row_data]
                self.model_4.appendRow(items)

            print('Search Results Fetched Successfully')
        except sqlite3.Error as e:
            print(f'Sqlite error: {e}')
        finally:
            conn.close()

    def delete_selected_row(self):
        # Get the selected row index
        selected_indexes = self.tableView_4.selectedIndexes()  # Assuming view_4 is your QTableView or similar
        if not selected_indexes:
            print("No row selected")
            return
        
        # Assuming the first column contains the ID and the second column contains the name
        selected_row = selected_indexes[0].row()
        member_id = self.model_4.item(selected_row, 0).text()
        member_name = self.model_4.item(selected_row, 1).text()
        
        # Show custom confirmation dialog with ID and name
        dialog = CustomConfirmDialog(member_id, member_name, self)
        reply = dialog.exec_dialog()
        
        if reply == QDialog.DialogCode.Accepted:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, 'members.db')
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()

            try:
                # Delete the member from the database
                cursor.execute("DELETE FROM members WHERE Id = ?", (member_id,))
                conn.commit()
                
                # Remove the row from the model
                self.model_4.removeRow(selected_row)
                print('Row Deleted Successfully')
            except sqlite3.Error as e:
                print(f'Sqlite error: {e}')
            finally:
                conn.close()
        else:
            print("Deletion cancelled")

    def back_manager_page(self):
        self.stackedWidget.setCurrentWidget(self.page_1)

    


if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    if login_dialog.exec() == QDialog.DialogCode.Accepted:
        main_app = MyApp(username=login_dialog.username)  # Pass the username
        main_app.show()
        main_app.show_frame()  # Show the frame only after successful authentication

    sys.exit(app.exec())