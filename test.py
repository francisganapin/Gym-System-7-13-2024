import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QHBoxLayout

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 200, 100)

        self.layout = QVBoxLayout()

        self.username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton('Login')

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)

        self.setLayout(self.layout)

        self.login_button.clicked.connect(self.check_credentials)

    def check_credentials(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Modify this with your authentication logic
        if username == "francis" and password == "francis":
            self.accept()
        else:
            self.username_input.clear()
            self.password_input.clear()
            self.username_input.setFocus()

class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('My Application')
        self.setGeometry(100, 100, 800, 600)

        self.main_layout = QVBoxLayout()

        self.label = QLabel("Welcome to MyApp!")
        self.main_layout.addWidget(self.label)

        self.frame = QFrame()
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_layout = QVBoxLayout()
        self.frame_label = QLabel("This is a secured frame!")
        self.frame_layout.addWidget(self.frame_label)
        self.frame.setLayout(self.frame_layout)

        self.main_layout.addWidget(self.frame)
        self.frame.hide()  # Hide the frame initially

        self.setLayout(self.main_layout)

    def show_frame(self):
        self.frame.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    if login_dialog.exec() == QDialog.DialogCode.Accepted:
        main_app = MyApp()
        main_app.show()
        main_app.show_frame()  # Show the frame only after successful authentication
  # Show the frame only after successful authentication

    sys.exit(app.exec())
