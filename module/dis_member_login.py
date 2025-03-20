import sys
from datetime import datetime
import os
import sqlite3
import csv

from PyQt6.QtCore import QTimer

from PyQt6.QtGui import QPixmap 
#################################third party import

from PyQt6.QtWidgets import QMessageBox

#################################


class LoginMemberDisplay:
    def __init__(self, ui):
        self.ui = ui

    def display_member_data(self):
            """display them if they are in login so that the 
            employee will know  if they are expired """
            member_id = self.ui.id_entry.text()
        
            member = self.fetch_data_member(member_id)
            
            if member:
                self.ui.name_label.setText(f"Name: {member[0]}")
            
                expiry_date_str = member[1]

                image_member = member[2]

                expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
                current_date = datetime.now().date()
                
                pixmap = QPixmap(image_member)
                self.ui.image_label.setPixmap(pixmap)

                if not os.path.exists(image_member):
                    self.ui.image_label.setText('image does not exist')
                    
                
                self.ui.expiry_label.setText(f"Expiry: {expiry_date_str}")
                print(image_member)

                
                if expiry_date < current_date:

                    self.ui.expiry_label.setStyleSheet("color: red; font: 900 italic 18pt")
                else:
                    self.ui.expiry_label.setStyleSheet("color: green; font: 900 italic 18pt")  # Reset to default color
            
                
                self.save_login_record(member[0])
                QTimer.singleShot(3000, lambda: self.ui.image_label.clear())
                QTimer.singleShot(3000, lambda: self.ui.name_label.clear())
                QTimer.singleShot(3000, lambda: self.ui.expiry_label.clear())
            else:
                QMessageBox.information(self, "Not Found", "Member not found.")


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
    
    def save_login_record(self, member_name):
        """
        this code if the person was login it would save at login_records.csv
        """
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record = [member_name, current_time,self.ui.username]

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