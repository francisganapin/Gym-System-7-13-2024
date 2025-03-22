import os
import sqlite3

from PyQt6.QtCore import QTimer

from PyQt6.QtGui import QStandardItem
from PyQt6.QtWidgets import (
QDialog, QLineEdit

)

from module.confirm_dialog import CustomConfirmDialog

class ManagerModule:
    def __init__(self, ui):
            self.ui = ui

    def check_credentials_manager(self):
            '''Check the credentials of the user'''
            self.manger = self.ui.username_input_2.text()
            password = self.ui.password_input_2.text()
            self.ui.password_input_2.setEchoMode(QLineEdit.EchoMode.Password)

            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, 'database.db')
        
            with sqlite3.connect(file_path) as conn:
                self.cursor = conn.cursor()

                query = 'SELECT * FROM users WHERE username = ? AND password = ?'

                self.cursor.execute(query, (self.ui.username, password))
                result = self.cursor.fetchone()

                if result:
                    self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
                else:
                    self.ui.username_input_2.text()
                    self.ui.password_input_2.text()
                    # Pop up invalid credentials
                    self.ui.invalid_label_2_manger.setText('Invalid Credentials')
                    QTimer.singleShot(3000, lambda: self.ui.invalid_label_2_manger.setText(''))

    def clear_credentials_manager(self):
        '''clear the input method'''
        self.ui.username_input_2.clear()
        self.ui.username_input_2.clear()
        self.ui.username_input_2.setFocus()

    def search_data_manger(self):
        """
        Search the data in the second tab. 
        You can choose to search by name or ID.
        """
        search_name_manger = self.ui.name_search_manger_input.text()
        search_id_manger = self.ui.id_search_manager_input.text()
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

            self.ui.model_4.removeRows(0, self.ui.model_4.rowCount())  # Clear the model

            for row_data in rows:
                items = [QStandardItem(str(data)) for data in row_data]
                self.ui.model_4.appendRow(items)

            print('Search Results Fetched Successfully')
        except sqlite3.Error as e:
            print(f'Sqlite error: {e}')
        finally:
            conn.close()

    def delete_selected_row(self):
        # Get the selected row index
        selected_indexes = self.ui.tableView_4.selectedIndexes()  # Assuming view_4 is your QTableView or similar
        if not selected_indexes:
            print("No row selected")
            return
            
            # Assuming the first column contains the ID and the second column contains the name
        selected_row = selected_indexes[0].row()
        member_id = self.ui.model_4.item(selected_row, 0).text()
        member_name = self.ui.model_4.item(selected_row, 1).text()
            
            # Show custom confirmation dialog with ID and name
        dialog = CustomConfirmDialog(member_id, member_name, self.ui)  # 
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
                self.ui.model_4.removeRow(selected_row)
                print('Row Deleted Successfully')
            except sqlite3.Error as e:
                print(f'Sqlite error: {e}')
            finally:
                conn.close()
        else:
            print("Deletion cancelled")


    
    def delete_database_manager(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, 'members.db')
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT Id, Name, Membership,Email, Expiry_date, Contact, Gender, Birthday, Address, Image FROM members")
            rows = cursor.fetchall()

            self.ui.model_4.removeRows(0, self.ui.model_4.rowCount())  # Clear the model

            for row_data in rows:
                items = [QStandardItem(str(data)) for data in row_data]
                self.ui.model_4.appendRow(items)

            print('Data Fetched Successfully')
        except sqlite3.Error as e:
            print(f'Sqlite error: {e}')
        finally:
            conn.close()







    def back_manager_page(self):
        self.stackedWidget.setCurrentWidget(self.page_1)
