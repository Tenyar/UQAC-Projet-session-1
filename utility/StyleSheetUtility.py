import sys
from PyQt5.QtWidgets import (
    QLabel, QWidget, QPushButton, QSpacerItem, QSizePolicy, QLineEdit
)

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QWidget
from PyQt5.QtCore import Qt, QEvent, QVariantAnimation
from PyQt5.QtGui import QColor, QPalette

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Importing DAO constants
from utility.StyleSheetConstantsUtility import *


# ---------------------------------------------------------------------------------------------------------
#   Utility class for building a user interface
# ---------------------------------------------------------------------------------------------------------
def create_background(MainWindow):
    MainWindow.setStyleSheet(f"""
            QMainWindow {{ background-color: {MAIN_BACKGROUND_COLOR}; }}
    """)


def create_h1_label(text):
    #   Creates and returns a QLabel styled like <h1>.
    label = QLabel(text)
    label.setStyleSheet(f"""
        QLabel {{
            font-size: {H1_FONT_SIZE};
            font-weight: {H1_FONT_WEIGHT};
            font-family: {FONT_FAMILY};
            padding: {H1_PADDING};
            color: {H1_COLOR};
            background-color: {H1_BACKGROUND_COLOR};
        }}
    """)
    return label


def create_h2_label(text):
     #   Creates and returns a QLabel styled like <h2>.
    label = QLabel(text)
    label.setStyleSheet(f"font-size: {H2_FONT_SIZE}; font-weight: {H2_FONT_WEIGHT}; font-family: {FONT_FAMILY}; color: {H2_COLOR};")
    return label


def create_paragraph_label(text):
    """Creates and returns a QLabel styled like a <p> paragraph."""
    label = QLabel(text)
    label.setStyleSheet(f"font-size: {P_FONT_SIZE}; font-family: {FONT_FAMILY}; color: {P_COLOR};")
    return label
     
     