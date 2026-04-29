import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QDesktopWidget, QWidget, QDialog, 
    QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox
)
from db import storage


def launch():
    """
    Start the PyQt application.

    Creates the application instance, initializes the main window,
    and starts the event loop.
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


class MainWindow(QWidget):
    """
    Main application window.

    Displays the welcome screen and provides navigation
    to login, signup, and probability preview features.
    """

    def __init__(self):
        """
        Initialize the main window UI components.
        """
        super().__init__()
        self.setWindowTitle("Probability App")
        self.setGeometry(200, 200, 450, 300)

        layout = QVBoxLayout()

        welcome_label = QLabel("Welcome to Probability Visualizer")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.open_login_window)
        layout.addWidget(login_btn)

        signup_btn = QPushButton("Sign Up")
        signup_btn.clicked.connect(self.open_signup_window)
        layout.addWidget(signup_btn)

        preview_btn = QPushButton("Preview Distributions")
        preview_btn.clicked.connect(self.open_preview_window)
        layout.addWidget(preview_btn)

        quit_btn = QPushButton("Quit")
        quit_btn.clicked.connect(self.close_window)
        layout.addWidget(quit_btn)

        self.setLayout(layout)
        self.center_window()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def open_login_window(self):
        """
        Handle login button click.

        Placeholder for login functionality.

        Future:
            Should open login dialog and call:
            storage.login(username, password)
        """
        print("Login clicked")

    def open_signup_window(self):
        """
        Open signup dialog.
        """
        dialog = SignupDialog()
        dialog.exec_()

    def open_preview_window(self):
        """
        Placeholder for probability distribution visualization.

        Future:
            Should open a new window displaying distributions.
        """
        print("Preview clicked")

    def close_window(self):
        """
        Closes the application.
        """
        self.close()


class SignupDialog(QDialog):
    """
    Dialog window for creating a new user.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Up")

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        signup_btn = QPushButton("Create Account")
        signup_btn.clicked.connect(self.handle_signup)
        layout.addWidget(signup_btn)

        self.setLayout(layout)

    def handle_signup(self):
        """
        Calls storage.add_user(username, password).

        Shows success or error popup based on result.
        """
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            storage.add_user(username, password)
            QMessageBox.information(
            self,
            "Success",
            "User created successfully"
        )
            self.accept()  # closes dialog

        except ValueError as e:
            QMessageBox.warning(
                self,
                "Error",
                str(e)
        )
