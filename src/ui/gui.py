import sys
from db import storage
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QDesktopWidget, QWidget, QDialog, 
    QVBoxLayout, QHBoxLayout, QFormLayout, 
    QPushButton, QLabel, QLineEdit, QMessageBox, QSpinBox, QDoubleSpinBox, QListWidget,
)
from plots import plots
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


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

def center_window(window):
    qr = window.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    window.move(qr.topLeft())

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
        self.current_user_id = None
        self.current_username = None
        self.setWindowTitle("Probability App")
        self.setGeometry(200, 200, 450, 300)

        layout = QVBoxLayout()

        self.user_status_label = QLabel("Not logged in")
        self.user_status_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.user_status_label)

        welcome_label = QLabel("Welcome to Probability Visualizer")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.open_login_window)
        layout.addWidget(self.login_btn)

        self.signup_btn = QPushButton("Sign Up")
        self.signup_btn.clicked.connect(self.open_signup_window)
        layout.addWidget(self.signup_btn)

        self.my_plots_btn = QPushButton("My Plots")
        self.my_plots_btn.clicked.connect(self.open_my_plots_window)
        self.my_plots_btn.hide()
        layout.addWidget(self.my_plots_btn)

        quit_btn = QPushButton("Quit")
        quit_btn.clicked.connect(self.close_window)
        layout.addWidget(quit_btn)

        self.setLayout(layout)
        center_window(self)

    def open_login_window(self):
        """
        Handle login button click.
        """
        dialog = LoginDialog()
        result = dialog.exec_()

        if result == QDialog.Accepted:
            self.current_user_id = dialog.user_id
            self.current_username = dialog.username
            self.user_status_label.setText(f"Logged in as: {self.current_username}")

            self.login_btn.setText("Logout")
            self.login_btn.clicked.disconnect()
            self.login_btn.clicked.connect(self.logout_user)

            self.signup_btn.hide()
            self.my_plots_btn.show()

    def logout_user(self):
        self.current_user_id = None
        self.current_username = None

        self.user_status_label.setText("Not logged in")

        self.login_btn.setText("Login")
        self.login_btn.clicked.disconnect()
        self.login_btn.clicked.connect(self.open_login_window)

        self.signup_btn.show()
        self.my_plots_btn.hide()

    def open_signup_window(self):
        """
        Open signup dialog.
        """
        dialog = SignupDialog()
        dialog.exec_()

    def open_my_plots_window(self):
        dialog = MyPlotsDialog(self.current_user_id)
        dialog.exec_()

    def close_window(self):
        """
        Closes the application.
        """
        self.close()

class LoginDialog(QDialog):
    """
    Dialog window for user login.
    """
    def __init__(self):
        super().__init__()
        self.user_id = None
        self.username = None
        self.setWindowTitle("Login")

        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)

        self.setLayout(layout)

    def handle_login(self):
        """
        Calls storage.authenticate_user(username, password).
        """
        username = self.username_input.text()
        password = self.password_input.text()

        user_id =  storage.authenticate_user(username, password)

        if user_id:
            self.user_id = user_id
            self.username = username

            QMessageBox.information(
            self,
            "Success",
            f"Welcome {username}!"
        )
            self.accept()  # closes dialog
        
        else:
            QMessageBox.warning(
                self,
                "Error",
                "Invalid username or password"
        )

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
        Calls storage.create_user(username, password).

        Shows success or error popup based on result.
        """
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            storage.create_user(username, password)
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

class MyPlotsDialog(QDialog):
    """
    Plot Viewer window for creating, viewing, and saving probability distributions.
    """
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

        self.setWindowTitle("Plot Viewer")
        self.setGeometry(200, 200, 1000, 700)
        center_window(self)

        main_layout = QHBoxLayout()

        # -------- Left Panel -------- #
        left_layout = QVBoxLayout()

        # Distribution selection
        distribution_label = QLabel("Distributions")
        left_layout.addWidget(distribution_label)

        self.distribution_list = QListWidget()
        self.distribution_list.addItems([
            "Normal Distribution",
            "Binomial Distribution",
            "Poisson Distribution"
        ])
        self.distribution_list.currentItemChanged.connect(
            self.on_distribution_selected
        )
        left_layout.addWidget(self.distribution_list)

        # Saved plots section
        saved_label = QLabel("Saved Plots")
        left_layout.addWidget(saved_label)

        self.saved_plots_list = QListWidget()
        self.saved_plots_list.itemClicked.connect(
            self.on_saved_plot_selected
        )
        left_layout.addWidget(self.saved_plots_list)

        delete_btn = QPushButton("Delete Plot")
        delete_btn.clicked.connect(self.delete_plot)
        left_layout.addWidget(delete_btn)

        # -------- Right Panel -------- #
        right_layout = QVBoxLayout()

        # Parameter controls
        self.parameter_layout = QFormLayout()
        right_layout.addLayout(self.parameter_layout)

        # Plot display area
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        right_layout.addWidget(self.canvas)

        # Save controls
        self.plot_name_input = QLineEdit()
        self.plot_name_input.setPlaceholderText("Enter plot name")
        right_layout.addWidget(self.plot_name_input)

        self.plot_description_input = QLineEdit()
        self.plot_description_input.setPlaceholderText("Enter plot description (optional)")
        right_layout.addWidget(self.plot_description_input)

        save_btn = QPushButton("Save Plot")
        save_btn.clicked.connect(self.save_plot)
        right_layout.addWidget(save_btn)

        # -------- Assemble Layout -------- #
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 3)

        self.setLayout(main_layout)
        self.load_plots()

    def on_distribution_selected(self):
        """
        Updates parameter controls based on selected distribution.
        """
        selected = self.distribution_list.currentItem()

        if not selected:
            return

        distribution = selected.text()

        # Clear old parameter controls
        while self.parameter_layout.rowCount():
            self.parameter_layout.removeRow(0)

        if distribution == "Normal Distribution":
            self.add_normal_parameters()

        elif distribution == "Binomial Distribution":
            self.add_binomial_parameters()

        elif distribution == "Poisson Distribution":
            self.add_poisson_parameters()

        self.update_plot_view()

    def on_saved_plot_selected(self):
        selected = self.saved_plots_list.currentItem()

        if not selected:
            return

        plot_id = selected.data(Qt.UserRole)
        plot = storage.get_plot_by_id(plot_id)

        if not plot:
            return

        distribution_type = plot[3]
        parameters = plot[4]

        # Select correct distribution
        matching_items = self.distribution_list.findItems(
            distribution_type,
            Qt.MatchExactly
        )

        if matching_items:
            self.distribution_list.blockSignals(True)
            self.distribution_list.setCurrentItem(matching_items[0])
            self.distribution_list.blockSignals(False)

            self.on_distribution_selected()

        # Populate parameters
        plots.apply_saved_plot_parameters(
            distribution_type,
            parameters,
            self
        )
        self.plot_name_input.setText(plot[1])
        self.plot_description_input.setText(plot[2])

        self.update_plot_view()
    
    def update_plot_view(self):
        """
        Draws selected distribution using current parameters.
        """
        selected = self.distribution_list.currentItem()

        if not selected:
            return

        distribution = selected.text()

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        if distribution == "Normal Distribution":
            mean = self.mean_input.value()
            std = self.std_input.value()

            x, y = plots.generate_normal_data(mean, std)

            ax.plot(x, y)
            ax.set_title("Normal Distribution")

            ax.set_xlim(min(x), max(x))
            ax.set_ylim(0, max(y) * 1.1)

        elif distribution == "Binomial Distribution":
            n = self.n_input.value()
            p = self.p_input.value()

            x, y = plots.generate_binomial_data(n, p)

            ax.bar(x, y)
            ax.set_title("Binomial Distribution")

        elif distribution == "Poisson Distribution":
            lam = self.lambda_input.value()

            x, y = plots.generate_poisson_data(lam)

            ax.bar(x, y)
            ax.set_title("Poisson Distribution")

        ax.grid(True)

        self.canvas.draw()
    
    def add_normal_parameters(self):

        self.mean_input = QDoubleSpinBox()
        self.mean_input.setRange(-1000, 1000)
        self.mean_input.setDecimals(2)
        self.mean_input.setSingleStep(0.1)
        self.mean_input.setValue(0.0)
        self.mean_input.valueChanged.connect(self.update_plot_view)

        self.std_input = QDoubleSpinBox()
        self.std_input.setRange(0.1, 1000)
        self.std_input.setDecimals(2)
        self.std_input.setSingleStep(0.1)
        self.std_input.setValue(1.0)
        self.std_input.valueChanged.connect(self.update_plot_view)

        self.parameter_layout.addRow("Mean (μ):", self.mean_input)
        self.parameter_layout.addRow("Std Dev (σ):", self.std_input)

    def add_binomial_parameters(self):
        
        self.n_input = QSpinBox()
        self.n_input.setMinimum(1)
        self.n_input.setValue(10)
        self.n_input.valueChanged.connect(self.update_plot_view)

        self.p_input = QDoubleSpinBox()
        self.p_input.setMinimum(0.0)
        self.p_input.setMaximum(1.0)
        self.p_input.setSingleStep(0.01)
        self.p_input.setValue(0.5)
        self.p_input.valueChanged.connect(self.update_plot_view)

        self.parameter_layout.addRow("Trials (n):", self.n_input)
        self.parameter_layout.addRow("Probability (p):", self.p_input)

    def add_poisson_parameters(self):
        self.lambda_input = QDoubleSpinBox()
        self.lambda_input.setMinimum(0.1)
        self.lambda_input.setValue(1.0)
        self.lambda_input.valueChanged.connect(self.update_plot_view)

        self.parameter_layout.addRow("Lambda (λ):", self.lambda_input)

    def load_plots(self):
        """
        Loads user's saved plots into saved plots list.
        """
        self.saved_plots_list.clear()

        plots = storage.get_user_plots(self.user_id)

        for plot in plots:
            plot_id = plot[0]
            plot_name = plot[1]
            distribution_type = plot[3]

            item_text = f"{plot_name} ({distribution_type})"

            self.saved_plots_list.addItem(item_text)

            item = self.saved_plots_list.item(
                self.saved_plots_list.count() - 1
            )
            item.setData(Qt.UserRole, plot_id)

        # Auto-load first plot if available
        if self.saved_plots_list.count() > 0:
            self.saved_plots_list.setCurrentRow(0)

    def save_plot(self):
        selected = self.distribution_list.currentItem()

        if not selected:
            QMessageBox.warning(self, "Error", "Select a distribution first.")
            return

        distribution = selected.text()

        plot_name = self.plot_name_input.text().strip()

        if not plot_name:
            QMessageBox.warning(self, "Error", "Plot name cannot be empty.")
            return

        parameters = plots.build_distribution_parameters(
            distribution,
            self
        )
        storage.create_plot(
            owner_id=self.user_id,
            plot_name=plot_name,
            description=self.plot_description_input.text().strip(),
            distribution_type=distribution,
            parameters=parameters
        )
        QMessageBox.information(
            self,
            "Success",
            "Plot saved successfully."
        )

        self.load_plots()
    
    def delete_plot(self):
        selected = self.saved_plots_list.currentItem()

        if not selected:
            QMessageBox.warning(
                self,
                "Error",
                "Select a saved plot to delete."
            )
            return

        plot_id = selected.data(Qt.UserRole)

        confirmation = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this plot?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            storage.delete_plot(plot_id)

            QMessageBox.information(
                self,
                "Success",
                "Plot deleted successfully."
            )
            self.load_plots()