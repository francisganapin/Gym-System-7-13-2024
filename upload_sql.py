import sys
import os
import shutil
import sqlite3
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget
)
from PyQt6.QtGui import QPixmap


class ImageUploader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Uploader")
        self.setGeometry(100, 100, 400, 300)

        # Designated folder to save images
        self.save_folder = "designated_folder"
        os.makedirs(self.save_folder, exist_ok=True)  # Ensure folder exists

        # Database setup
        self.database = "image_metadata.db"
        self.setup_database()

        # Temporary storage for selected image
        self.selected_image_path = None

        # UI Elements
        self.layout = QVBoxLayout()

        self.image_label = QLabel("No Image Selected")
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(300, 200)

        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.upload_image)

        self.save_button = QPushButton("Save Image")
        self.save_button.setEnabled(False)  # Initially disabled
        self.save_button.clicked.connect(self.save_image)

        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.upload_button)
        self.layout.addWidget(self.save_button)

        # Set central widget
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def setup_database(self):
        """Initialize the database and create the table."""
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                save_path TEXT NOT NULL,
                upload_date TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def upload_image(self):
        """Select an image and display it without saving."""
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]  # Get the selected file path
            self.selected_image_path = file_path

            # Display image in QLabel
            pixmap = QPixmap(file_path).scaled(
                self.image_label.width(), self.image_label.height()
            )
            self.image_label.setPixmap(pixmap)

            # Enable the save button
            self.save_button.setEnabled(True)

    def save_image(self):
        """Save the selected image and its metadata."""
        if self.selected_image_path:
            # Save the image to the designated folder
            save_path = os.path.join(self.save_folder, os.path.basename(self.selected_image_path))
            shutil.copy(self.selected_image_path, save_path)

            # Save metadata to the database
            self.save_to_database(os.path.basename(self.selected_image_path), save_path)

            print(f"Image saved to: {save_path}")

            # Reset after saving
            self.selected_image_path = None
            self.image_label.setText("No Image Selected")
            self.image_label.clear()
            self.save_button.setEnabled(False)

    def save_to_database(self, filename, save_path):
        """Insert image metadata into the database."""
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO images (filename, save_path, upload_date)
            VALUES (?, ?, ?)
        """, (filename, save_path, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        print(f"Metadata saved to database: {filename}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageUploader()
    window.show()
    sys.exit(app.exec())
