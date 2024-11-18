import sys
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QVBoxLayout,
    QLabel, QWidget, QPushButton, QSpacerItem, QSizePolicy, QLineEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Add the project root directory to sys.path (for importing custom classes)
sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import utility.StyleSheetUtility as windowUtils
import utility.InputUtility as inputUtils
import utility.ButtonUtility as ButtonUtils


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("[Prototype] Login")
        self.setGeometry(100, 100, 1024, 1024)

        # Créer le widget de conteneur pour changer de vue
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        windowUtils.create_background(self)

        # Créer les différentes pages
        self.login_page = self.create_login_page()
        self.user_page = self.create_user_page()
        self.generate_password = self.create_user_page()
        self.chest_password = self.create_user_page()

        # Ajouter les pages au QStackedWidget
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.user_page)


    def create_login_page(self):
        # Créer la page d'accueil
        login_page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Removes all margins around the layout
        label =  windowUtils.create_h1_label("Login/Sign in") #    QLabel("<h1>Login/Sign in</h1>")
        label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)  # Aligner en haut au centre
        # Ajouter le label au layout
        layout.addWidget(label)
        # Ajouter un espacement entre le label et le bouton
        spacer = QSpacerItem(20, 200, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        # Username input
        username_input = inputUtils.InputUtility('Username/Email', self)
        username_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # horizontal and vertical expansion
        layout.addWidget(username_input, alignment=QtCore.Qt.AlignCenter)


        # Password input
        password_input = inputUtils.InputUtility('Password', self)
        password_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # horizontal and vertical expansion
        password_input.setEchoMode(QLineEdit.Password)  # Hide password input
        layout.addWidget(password_input, alignment=QtCore.Qt.AlignCenter)

        # Set size policy to expanding so they resize with the window
        username_input.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        password_input.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        #//button = QPushButton("Login")
        button_login = ButtonUtils.ButtonUtility('Login', self, True)
        button_login.clicked.connect(self.show_profile_page)
        # Ajouter le widget bouton au layout
        layout.addWidget(button_login, alignment=Qt.AlignCenter)
        # Set size policy to expanding so they resize with the window
        button_login.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # Ajouter un espace vide en bas pour forcer le label à rester en haut
        layout.addStretch()

        login_page.setLayout(layout)
        return login_page


    def create_user_page(self):
        # Créer la page de profil
        profile_page = QWidget()
        layout = QVBoxLayout()
       #// layout.setContentsMargins(0, 0, 0, 0)  # Removes all margins around the layout

        label = QLabel("Welcome to user Login")
        button = QPushButton("Logout")
        button.clicked.connect(self.show_home_page)

        layout.addWidget(label)
        layout.addWidget(button)
        profile_page.setLayout(layout)
        return profile_page


    def show_home_page(self):
        # Basculer vers la page d'accueil
        self.stacked_widget.setCurrentWidget(self.login_page)


    def show_profile_page(self):
        # Basculer vers la page de profil
        self.stacked_widget.setCurrentWidget(self.user_page)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())