from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QLineEdit
from utility.StyleSheetConstantsUtility import (
    INPUT_BORDER, INPUT_BACKGROUND_COLOR, INPUT_HOVER_BACKGROUND_COLOR, INPUT_HOVER_TEXT_COLOR, INPUT_BORDER_RADIUS, INPUT_WEIGHT, FONT_FAMILY
)


#   Utility class to create PyQt5 inputs fields
class InputUtility(QLineEdit):
    def __init__(self, placeholder, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        
        # Animation setup for background and text color transition
        self.animation_on_hover = QtCore.QVariantAnimation(
            startValue=QtGui.QColor(INPUT_BACKGROUND_COLOR),
            endValue=QtGui.QColor(INPUT_HOVER_BACKGROUND_COLOR),
            valueChanged=self._on_value_changed, #  Handled when the event is triggered (accepting parameter color dynamically)
            duration=125,
        )
        
        # Set the initial style
        self._update_stylesheet(QtGui.QColor(INPUT_BACKGROUND_COLOR), QtGui.QColor("black"))
        
        # Set size for the input field
        self.setFixedSize(450, 50)  # Set fixed size (Width: 300px, Height: 50px)

        # Set cursor to I-beam by default (input cursor)
        self.setCursor(QtCore.Qt.IBeamCursor)

        self.setContentsMargins(50, 0, 10, 0)  # Removes all margins around the layout


    def resizeEvent(self, event):
            # Calculate margins as a percentage of the window's width
            margin_size = int(self.width() * 0.01)  # 5% of the window's width

            # Update the layout margins
            self.setContentsMargins(margin_size, margin_size, margin_size, margin_size)

            # Call the base class resize event
            super().resizeEvent(event)


    def _on_value_changed(self, color):
        foreground = (
            QtGui.QColor("INPUT_HOVER_TEXT_COLOR") #    Ternary expression used for simplification
            if self.animation_on_hover.direction() == QtCore.QAbstractAnimation.Forward
            else QtGui.QColor("black")
        )
        self._update_stylesheet(color, foreground)


    def _update_stylesheet(self, background, foreground):
        # Update the stylesheet dynamically with the animation color values
        self.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: {background.name()};
                border: {INPUT_BORDER};
                color: {foreground.name()};
                border-radius: {INPUT_BORDER_RADIUS};
                font-weight: {INPUT_WEIGHT};
                font-family: {FONT_FAMILY};
            }}
            """
        )


    def enterEvent(self, event):
        # Change cursor to I-beam when the mouse hovers over the input field
        self.setCursor(QtCore.Qt.IBeamCursor)
        
        # Start animation in the forward direction (hover effect)
        self.animation_on_hover.setDirection(QtCore.QAbstractAnimation.Forward)
        self.animation_on_hover.start()
        super().enterEvent(event)


    def leaveEvent(self, event):
        # Change cursor back to I-beam when mouse leaves the input field
        self.setCursor(QtCore.Qt.IBeamCursor)
        
        # Start animation in the backward direction (revert effect)
        self.animation_on_hover.setDirection(QtCore.QAbstractAnimation.Backward)
        self.animation_on_hover.start()
        super().leaveEvent(event)