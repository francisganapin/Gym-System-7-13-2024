import sys
from PyQt6 import QtWidgets,uic
import os
import sqlite3
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QDateEdit
from PyQt6.QtCore import Qt,QDate
from PyQt6.QtWidgets import QMessageBox
from tkinter import messagebox

class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('gym.ui', self)
       
        # Assuming you have a QTableView in your UI file named 'tableView'
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Id", "Name", "Email", "Expiry_date", "Contact", "Gender", "Birthday", "Address"])
        self.tableView.setModel(self.model)
        self.tableView_2.setModel(self.model)

        # Load the data when the application starts
        self.showDatabase()

        self.SearchButton.clicked.connect(self.search_data)
        self.register_button.clicked.connect(self.InserData)
        self.Save_Date_Bt.clicked.connect(self.edit_item)
        self.Login_bt.clicked.connect(self.display_member_data)
        self.showDatabase()

        ##### this would we should add this so our  display fucntion would work
        self.name_label = self.findChild(QtWidgets.QLabel,'name_label')
        self.expiry_label = self.findChild(QtWidgets.QLabel,'expiry_label')

    def InserData(self):
        ###############################################################
        #self.id_input.setObjectName("id_input") line 55
        id    = self.id_input.text()
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

        member_id  = self.id_entry.text()     


        current_directory = os.path.dirname(os.path.abspath(__file__))

        file_path = os.path.join(current_directory,'members.db')
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''INSERT INTO members(Id,Name,Email,Expiry_date,Contact,Gender,Birthday,Address)
                        VALUES(?,?,?,?,?,?,?,?)''', (id, name, email, expiry_date, contact, gender, birthday, address))
            conn.commit()
            print('Data Inserted Successfully')
        except sqlite3.IntegrityError as e:
            print(f'Sqlite error: {e}')
        finally:
            conn.close()


        print(f"{id},{name},{email},{expiry_date},{birthday},{gender},{member},{address}")
        
    #this will fetch the data on the 
    def showDatabase(self):
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
    
    #this was the code that i use to edit the table since 
    def edit_item(self):
        selected_index = self.tableView_2.selectionModel().currentIndex()
        if not selected_index.isValid():
            QMessageBox.warning(self, "Selection Error", "Please select a row to edit.")
            return
        
        selected_row = selected_index.row()
        item_id = self.model.item(selected_row, 0).text()
        new_expiry = self.Expiry_edit.selectedDate().toString("yyyy-MM-dd")
        
        self.model.setItem(selected_row, 3, QStandardItem(new_expiry))  # Assuming column 3 is Expiry

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
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            conn.close()


    def fetch_data_member(self, member_id):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'members.db')
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        cursor.execute('SELECT Name, Expiry_date FROM members WHERE Id = ?', (member_id,))
        member = cursor.fetchone()
        conn.close()
        return member

    def display_member_data(self):
        member_id = self.id_entry.text()
        
        member = self.fetch_data_member(member_id)
        if member:
            self.name_label.setText(f"Name: {member[0]}")
            self.expiry_label.setText(f"Expiry: {member[1]}")
        else:
            QMessageBox.information(self, "Not Found", "Member not found.")



        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())