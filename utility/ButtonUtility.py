from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QPushButton
from utility.StyleSheetConstantsUtility import (
    BUTTON_BORDER, BUTTON_BORDER_RADIUS, BUTTON_COLOR_ACCEPT, BUTTON_COLOR_HOVER_ACCEPT, BUTTON_COLOR_REFUSE, BUTTON_COLOR_HOVER_REFUSE,
    INPUT_WEIGHT, FONT_FAMILY
)


#   Utility class to create PyQt5 buttons
class ButtonUtility(QPushButton):
    def __init__(self, name_of_button, parent=None, accept_or_refuse=True):
        super().__init__(parent)
        
        # Set the button text
        self.setText(name_of_button)
        
        if accept_or_refuse:
            self.BUTTON_BACKGROUND_COLOR = BUTTON_COLOR_ACCEPT
            # Animation setup for background and text color transition
            self.animation_on_hover = QtCore.QVariantAnimation(
                startValue=QtGui.QColor(BUTTON_COLOR_ACCEPT),
                endValue=QtGui.QColor(BUTTON_COLOR_HOVER_ACCEPT),
                valueChanged=self._on_value_changed,
                duration=125,
            )
            # Set the initial style
            self._update_stylesheet(QtGui.QColor(BUTTON_COLOR_ACCEPT), QtGui.QColor("white"))
        else:
            self.BUTTON_BACKGROUND_COLOR = BUTTON_COLOR_REFUSE
            self.animation_on_hover = QtCore.QVariantAnimation(
                startValue=QtGui.QColor(BUTTON_COLOR_REFUSE),
                endValue=QtGui.QColor(BUTTON_COLOR_HOVER_REFUSE),
                valueChanged=self._on_value_changed,
                duration=125,
            )
            # Set the initial style
            self._update_stylesheet(QtGui.QColor(BUTTON_COLOR_REFUSE), QtGui.QColor("white"))
        
        # Set size for the button
        self.setFixedSize(450, 50)
        self.setContentsMargins(10, 0, 10, 0)  # Removes all margins around the layout


    def resizeEvent(self, event):
            # Calculate margins as a percentage of the window's width
            margin_size = int(self.width() * 0.05)  # 5% of the window's width

            # Update the layout margins
            self.setContentsMargins(margin_size, margin_size, margin_size, margin_size)

            # Call the base class resize event
            super().resizeEvent(event)


    def _on_value_changed(self, color):
        foreground = (
            QtGui.QColor("white") #    Ternary expression used for simplification
            if self.animation_on_hover.direction() == QtCore.QAbstractAnimation.Forward
            else QtGui.QColor("white")
        )
        self._update_stylesheet(color, foreground)


    def _update_stylesheet(self, background, foreground):
        # Update the stylesheet dynamically with the animation color values
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {background.name()};
                border: {BUTTON_BORDER};
                color: {foreground.name()};
                border-radius: {BUTTON_BORDER_RADIUS};
                font-weight: {INPUT_WEIGHT};
                font-family: {FONT_FAMILY};
            }}
            """
        )


    def enterEvent(self, event):
        # Change cursor to hand on hover
        self.setCursor(QtCore.Qt.PointingHandCursor)
        # Start animation in the forward direction (hover effect)
        self.animation_on_hover.setDirection(QtCore.QAbstractAnimation.Forward)
        self.animation_on_hover.start()
        super().enterEvent(event)


    def leaveEvent(self, event):
        # Change cursor back to default
        self.unsetCursor()
        # Start animation in the backward direction (revert effect)
        self.animation_on_hover.setDirection(QtCore.QAbstractAnimation.Backward)
        self.animation_on_hover.start()
        super().leaveEvent(event)