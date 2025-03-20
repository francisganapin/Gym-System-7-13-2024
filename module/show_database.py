import os
import sqlite3
#################################third party import
from PyQt6.QtGui import  QStandardItem
from PyQt6.QtWidgets import QMessageBox
#################################


class ShowDatabaseDisplay:
    def __init__(self, ui):
        self.ui = ui



    def show_database(self):
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, 'members.db')
            conn = sqlite3.connect(file_path)
            cursor = conn.cursor()

            try:
                cursor.execute("SELECT Id, Name, Membership,Email, Expiry_date, Contact, Gender, Birthday, Address,Image FROM members")
                rows = cursor.fetchall()

                self.ui.model_1.removeRows(0, self.ui.model_1.rowCount())  # Clear the model

                for row_data in rows:
                    items = [QStandardItem(str(data)) for data in row_data]
                    self.ui.model_1.appendRow(items)

                for row_data in rows:
                    items = [QStandardItem(str(data)) for data in row_data]
                    self.ui.model_2.appendRow(items)

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
        search_name = self.ui.name_search_input.text()
        search_id = self.ui.id_search_input.text()
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

            self.ui.model_2.removeRows(0, self.ui.model_2.rowCount())  # Clear the model

            for row_data in rows:
                items = [QStandardItem(str(data)) for data in row_data]
                self.ui.model_2.appendRow(items)

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
        
        selected_index = self.ui.tableView_2.selectionModel().currentIndex()
        selected_row = selected_index.row()
        # Check if a valid row is selected
        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "No row is selected.")
            return
        item_id = self.ui.model_2.item(selected_row, 0).text()
        # Check if item_id is valid (not empty)
        if not item_id:
            QMessageBox.warning(self, "Selection Error", "No item is selected.")
            return
        new_expiry = self.ui.Expiry_edit.selectedDate().toString("yyyy-MM-dd")
        # Update the model in the table view
        self.ui.model_2.setItem(selected_row,3,QStandardItem(new_expiry))  # Assuming column 3 is Expiry
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