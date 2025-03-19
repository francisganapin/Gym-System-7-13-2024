import os
import sqlite3
from PyQt6.QtWidgets import QMessageBox
from .missing_value import MissingValueDialog

from PyQt6.QtCore import QDate
import os
import sqlite3

from PIL import Image

from PyQt6.QtGui import QPixmap 
#################################third party import

from PyQt6.QtWidgets import QMessageBox

#################################
from PyQt6.QtWidgets import  QFileDialog

class InsertValue:
    def __init__(self, ui):
        self.ui = ui

    def upload_image(self):
        """Open a file dialog to select an image and display it in QLabel (image_label_2)."""
         # initialize save path
        self.save_path = None
        # Create a QFileDialog instance
        file_dialog = QFileDialog(self.ui)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)  # Allow only existing files
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")  # Filter to show image files
        
        if file_dialog.exec():  # Open the dialog and wait for user interaction
            file_path_image = file_dialog.selectedFiles()[0]  # Get the selected file path
            
            # Display the selected image in the QLabel (image_label_2)
            pixmap = QPixmap(file_path_image).scaled(
                self.ui.image_label_2.width(), self.ui.image_label_2.height()
            )
            self.ui.image_label_2.setPixmap(pixmap)
            

            # Optionally store the path for further actions
            self.selected_image_path = file_path_image
            

            # Save the image to the designated folder
            save_path = os.path.join(self.ui.save_folder, os.path.basename(self.selected_image_path))

            #save the image
            with Image.open(file_path_image) as img:
                img = img.convert('RGB')
                resize_img = img.resize((451,241))
                resize_img.save(save_path)


            self.save_path = save_path
            print(f"Image saved to: {save_path}")

            # we need convert image to 516 * 516  3/18/2025


    def insert_data(self):
            '''
            this one is use for register data of the member
            '''
  

            id_value    = self.ui.id_input.text()
            name =  self.ui.name_input.text()
            email = self.ui.email_input.text()
            expiry_date = self.ui.expiry_input.selectedDate().toString("yyyy-MM-dd") 
            birthday =  self.ui.birthday_input.selectedDate().toString("yyyy-MM-dd") 
            gender = self.ui.gender_input.currentText()
            member = self.ui.member_input.currentText()
            address = self.ui.address_input.toPlainText()
            contact   = self.ui.contact_input.text()
            path_image_data = self.ui.save_path

            # we need to fix this mix value show what the value missing here
            list_values ={
                'ID Card':id_value,
                'Name':name,
                'Email':email,
                'Expiry':expiry_date,
                'Birthday':birthday,
                'Member':member,
                'Address':address,
                'Contact':contact,
                'Profile':self.save_path
            }  
            
            # Check all values before filtering
            print(f"Debug: All values -> {list_values}")

                    # Collect missing fields where values are empty
            missing_values = [key for key, val in list_values.items() if not val or str(val).strip() == ""]

                    # Debugging print
            print(f"Debug: Missing values list -> {missing_values}")

            if missing_values:
                value = ', '.join(missing_values)  # Properly format with commas
                print(f'There are missing values: {value}')  # Debugging output
                dialog = MissingValueDialog(f'There are missing values: {value}')
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

        self.ui.contact_input.clear()
        self.ui.id_input.clear()
        self.ui.name_input.clear()
        self.ui.email_input.clear()
        self.ui.expiry_input.setSelectedDate(QDate.currentDate())
        self.ui.birthday_input.setSelectedDate(QDate.currentDate())
        self.ui.gender_input.currentText()
        self.ui.member_input.currentText()
        self.ui.address_input.clear()
        self.ui.contact_input.clear()
        self.ui.image_label_2.clear()