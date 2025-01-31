import sys
from datetime import datetime
import os
import sqlite3
import csv
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
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QPushButton
import shutil
from PyQt6.QtCore import QDate

class LoginDialog(QDialog):
    '''Display data and this was the framework of our app before they can login'''
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)

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

    def clear_credentials(self):
        '''clear the input method'''
        self.username_input.clear()
        self.password_input.clear()
        self.username_input.setFocus()

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



class MissingValueDialog(QDialog):
    def __init__(self, message, parent=None):
        super().__init__(parent)

        
        self. setWindowTitle('Missing Values')
        self.setFixedSize(300,150)
        layout = QVBoxLayout()

        self.message_label = QLabel(message)
        layout.addWidget(self.message_label)


        self.ok_button = QPushButton('ok')
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)


    def exec_dialog(self):
        return self.exec()


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
        # Assuming you have a QTableView in your UI file named 'tableView'
        self.model_1 = QStandardItemModel()
        self.model_1.setHorizontalHeaderLabels(["Id","Name",'Membership',"Email", "Expiry_date", "Contact", "Gender", "Birthday", "Address","Image"])
        self.tableView.setModel(self.model_1)

        self.model_2 = QStandardItemModel()
        self.model_2.setHorizontalHeaderLabels(["Id","Name",'Membership',"Email", "Expiry_date", "Contact", "Gender", "Birthday", "Address","Image"])
        self.tableView_2.setModel(self.model_2)
        
        self.model_4 = QStandardItemModel()
        self.model_4.setHorizontalHeaderLabels(["Id","Name",'Membership',"Email", "Expiry_date", "Contact", "Gender","Birthday", "Address","Image"])
        self.tableView_4.setModel(self.model_4)

        # Load the data when the application starts
        self.show_database()
        self.delete_database_manager()

        self.SearchButton.clicked.connect(self.search_data)
        self.register_button.clicked.connect(self.insert_data)
        self.Save_Date_Bt.clicked.connect(self.edit_item)
        self.Login_bt.clicked.connect(self.display_member_data)
        self.login_button_2.clicked.connect(self.check_credentials_manager)
        self.search_bt_manager.clicked.connect(self.search_data_manger)
        self.delete_bt_manager_2.clicked.connect(self.delete_selected_row)
        self.back_bt_manager.clicked.connect(self.back_manager_page)
        self.upload_button_2.clicked.connect(self.upload_image)
        
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
        
    def upload_image(self):
        """Open a file dialog to select an image and display it in QLabel (image_label_2)."""
        # Create a QFileDialog instance
        file_dialog = QFileDialog(self)  
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)  # Allow only existing files
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")  # Filter to show image files
        
        if file_dialog.exec():  # Open the dialog and wait for user interaction
            file_path_image = file_dialog.selectedFiles()[0]  # Get the selected file path
            
            # Display the selected image in the QLabel (image_label_2)
            pixmap = QPixmap(file_path_image).scaled(
                self.image_label_2.width(), self.image_label_2.height()
            )
            self.image_label_2.setPixmap(pixmap)

            # Optionally store the path for further actions
            self.selected_image_path = file_path_image
            

            # Save the image to the designated folder
            save_path = os.path.join(self.save_folder, os.path.basename(self.selected_image_path))
            shutil.copy(self.selected_image_path, save_path)

            self.save_path = save_path
            print(f"Image saved to: {save_path}")

    def insert_data(self):
        '''
        this one is use for register data of the member
        '''
     
        id_value    = self.id_input.text()
        name =  self.name_input.text()
        email = self.email_input.text()
        expiry_date = self.expiry_input.selectedDate().toString("yyyy-MM-dd") 
        birthday =  self.birthday_input.selectedDate().toString("yyyy-MM-dd") 
        gender = self.gender_input.currentText()
        member = self.member_input.currentText()
        address = self.address_input.toPlainText()
        contact   = self.contact_input.text()
        path_image_data = self.save_path


        if not hasattr(self,'save_path') or not self.save_path:
            dialog = MissingValueDialog('missing image value')
            dialog.exec_dialog()
            return

        if not all([id_value,name,email,expiry_date,birthday,member,address,contact,self.save_path]):
            dialog = MissingValueDialog('there are missing value')
            dialog.exec_dialog()
            return
        
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory,'members.db')
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''INSERT INTO members
                        (Id,Name,Membership,Email,Expiry_date,Contact,Gender,Birthday,Address,Image)
                        VALUES(?,?,?,?,?,?,?,?,?,?)''', 
                        (id_value,name,member,email,expiry_date,contact,gender,birthday,address,path_image_data))

            print('Data Inserted Successfully')
            self.clear_data_input()
            conn.commit()
           
        except sqlite3.IntegrityError:
           QMessageBox.warning(self, "Duplicate Id", f"An entry with ID {id_value} is already exists.")
        finally:
            conn.close()

    def clear_data_input(self):
        """this will clear the data input text"""

        self.contact_input.clear()
        self.id_input.clear()
        self.name_input.clear()
        self.email_input.clear()
        self.expiry_input.setSelectedDate(QDate.currentDate())
        self.birthday_input.setSelectedDate(QDate.currentDate())
        self.gender_input.currentText()
        self.member_input.currentText()
        self.address_input.clear()
        self.contact_input.clear()
        self.image_label_2.clear()

    def show_database(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'members.db')
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT Id, Name, Membership,Email, Expiry_date, Contact, Gender, Birthday, Address,Image FROM members")
            rows = cursor.fetchall()

            self.model_1.removeRows(0, self.model_1.rowCount())  # Clear the model

            for row_data in rows:
                items = [QStandardItem(str(data)) for data in row_data]
                self.model_1.appendRow(items)

            for row_data in rows:
                items = [QStandardItem(str(data)) for data in row_data]
                self.model_2.appendRow(items)

            print('Data Fetched Successfully')
        except sqlite3.Error as e:
            print(f'Sqlite error: {e}')
        finally:
            conn.close()

 

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

    def search_data(self):
        """
        Search the data in the second tab. 
        You can choose to search by name or ID.
        """
        search_name = self.name_search_input.text()
        search_id = self.id_search_input.text()
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'members.db')
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        query = "SELECT Id, Name, Email, Membership,Expiry_date, Contact, Gender, Birthday, Address FROM members WHERE 1=1"
        params = []

        if search_name:
            query += " AND Name LIKE ?"
            params.append(f"%{search_name}%")

        if search_id:
            query += " AND Id = ?"
            params.append(search_id)

        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()

            self.model_2.removeRows(0, self.model_2.rowCount())  # Clear the model

            for row_data in rows:
                items = [QStandardItem(str(data)) for data in row_data]
                self.model_2.appendRow(items)

            print('Search Results Fetched Successfully')
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

    def fetch_data_member(self, member_id):
        """
        this one is for function for display_member_data()
        since this one it will use for fetching member in login
        """
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'members.db')
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        cursor.execute('SELECT Name, Expiry_date,Image FROM members WHERE Id = ?', (member_id,))
        member = cursor.fetchone()
        conn.close()
        return member

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