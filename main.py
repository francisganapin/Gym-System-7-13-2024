import sys
from datetime import datetime
import os
import sqlite3
import csv


#################################third party import
from PyQt6.QtWidgets import QApplication, QDialog, QLineEdit
from PyQt6 import QtWidgets,uic
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QMessageBox
#################################

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
        '''check the credential of the user'''
        username = self.username_input.text()
        password = self.password_input.text()

        # Modify this with your authentication logic
        if username == "francis" and password == "francis":
            self.accept()
        else:
            self.username_input.clear()
            self.password_input.clear()
            self.username_input.setFocus()

    def clear_credentials(self):
        '''clear the input method'''
        self.username_input.clear()
        self.password_input.clear()
        self.username_input.setFocus()

class MyApp(QtWidgets.QWidget):
    ''' display oru data so that it would work
    '''
    def __init__(self):
        super().__init__()
        uic.loadUi('gym.ui', self)
       
        # Set fixed size to prevent resizing
        self.setFixedSize(self.size())

        # Apply the dark theme
        # Assuming you have a QTableView in your UI file named 'tableView'
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Id","Name", "Email", "Expiry_date", "Contact", "Gender", "Birthday", "Address"])
        self.tableView.setModel(self.model)
        self.tableView_2.setModel(self.model)
        
        # Load the data when the application starts
        self.show_database()

        self.SearchButton.clicked.connect(self.search_data)
        self.register_button.clicked.connect(self.insert_data)
        self.Save_Date_Bt.clicked.connect(self.edit_item)
        self.Login_bt.clicked.connect(self.display_member_data)

        self.tableView_3_model = QStandardItemModel()
        self.tableView_3.setModel(self.tableView_3_model)

        # Load login records initially
        self.display_login_records()


        ##### this would we should add this so our  display fucntion would work
       

    def insert_data(self):
        '''
        this one is use for register data of the member
        '''
        ###############################################################
        #self.id_input.setObjectName("id_input") line 55
        id_value    = self.id_input.text()
        ###############################################################
        #self.name_input.setObjectName("name_input") line 46
        name =  self.name_input.text()
        ###############################################################
        #self.email_input.setObjectName("email_input") lien 24
        email = self.email_input.text()
        ###############################################################
        #self.birthday_widget.setObjectName("birthday_widget") line 67
        expiry_date = self.expiry_input.selectedDate().toString("yyyy-MM-dd") 
        ###############################################################
        #self.birthday_widget.setObjectName("birthday_widget") 64
        birthday =  self.expiry_input.selectedDate().toString("yyyy-MM-dd") 
        ###############################################################
        #self.gender_input.setObjectName("gender_input") line 30
        #self.member_input.addItem("")
        #self.member_input.addItem("")
        #it was qcombox use current text
        gender = self.gender_input.currentText()
        ################################################################
        #self.member_input.setObjectName("member_input") 35
        member = self.member_input.currentText()
        ################################################################
        #.toPlainText() use to plain text if we using textEdit
        address = self.address_input.toPlainText()
        ###############################################################
        #self.contact_input.setObjectName("contact_input")65
        contact   = self.contact_input.text()
        ###############################################################
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory,'members.db')
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''INSERT INTO members
                        (Id,Name,Email,Expiry_date,Contact,Gender,Birthday,Address)
                        VALUES(?,?,?,?,?,?,?,?)''', 
                        (id_value,name,email,expiry_date, contact,gender,birthday,address))
            
            conn.commit()
            print('Data Inserted Successfully')
        except sqlite3.IntegrityError:
           QMessageBox.warning(self, "Duplicate Id", f"An entry with ID {id} already exists.")
        finally:
            conn.close()


        print(f"{id},{name},{email},{expiry_date},{birthday},{gender},{member},{address}")
  
    def show_database(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'members.db')
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT Id, Name, Email, Expiry_date, Contact, Gender, Birthday, Address FROM members")
            rows = cursor.fetchall()

            self.model.removeRows(0, self.model.rowCount())  # Clear the model

            for row_data in rows:
                items = [QStandardItem(str(data)) for data in row_data]
                self.model.appendRow(items)

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

        query = "SELECT Id, Name, Email, Expiry_date, Contact, Gender, Birthday, Address FROM members WHERE 1=1"
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

            self.model.removeRows(0, self.model.rowCount())  # Clear the model

            for row_data in rows:
                items = [QStandardItem(str(data)) for data in row_data]
                self.model.appendRow(items)

            print('Search Results Fetched Successfully')
        except sqlite3.Error as e:
            print(f'Sqlite error: {e}')
        finally:
            conn.close()

    
  
    def edit_item(self):
        '''this one is edit for data on selected member 
            in order to update the data it should specify the 
            target member
        '''
        
        selected_index = self.tableView_2.selectionModel().currentIndex()
        selected_row = selected_index.row()
        # Check if a valid row is selected
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "No row is selected.")
            return
        item_id = self.model.item(selected_row, 0).text()
        # Check if item_id is valid (not empty)
        if not item_id:
            QMessageBox.warning(self, "Selection Error", "No item is selected.")
            return
        new_expiry = self.Expiry_edit.selectedDate().toString("yyyy-MM-dd")
        # Update the model in the table view
        self.model.setItem(selected_row,3,QStandardItem(new_expiry))  # Assuming column 3 is Expiry
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
        cursor.execute('SELECT Name, Expiry_date FROM members WHERE Id = ?', (member_id,))
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
            self.expiry_label.setText(f"Expiry: {member[1]}")
        else:
            QMessageBox.information(self, "Not Found", "Member not found.")

    def save_login_record(self, member_name):
        """
        this code if the person was login it would save at login_records.csv
        """
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record = [member_name, current_time]

            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, 'login_records.csv')

            file_exists = os.path.isfile(file_path)
            with open(file_path, 'a', newline='',encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Name", "Login Time"])
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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    if login_dialog.exec() == QDialog.DialogCode.Accepted:
        main_app = MyApp()
        main_app.show()
        main_app.show_frame()  # Show the frame only after successful authentication

    sys.exit(app.exec())