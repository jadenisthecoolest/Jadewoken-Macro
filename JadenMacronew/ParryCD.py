import sys
import time
import win32gui
import win32con
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor
import keyboard  # To detect key presses

class Overlay(QWidget):
    def __init__(self):
        super().__init__()

        # Set up overlay window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, 1920, 1080)  # Adjust based on screen size

        # Make window click-through
        hwnd = self.winId()
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, 
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)

        # Bar settings
        self.bar_width = 400
        self.bar_height = 25
        self.bar_x = (1920 - self.bar_width) // 2  # Centered
        self.bar_y = 350  # Adjust vertical position
        self.bar_value = 100  # Full at 100%
        self.bar_decrease_amount = 100  # Instant drain on 'F'
        self.bar_refill_speed = 2  # How fast it refills (higher = slower)

        # Timer for refill
        self.timer = QTimer()
        self.timer.timeout.connect(self.refill_bar)
        self.timer.start(20)  # Update every 20ms

        # Listen for key press
        keyboard.on_press_key("f", self.drain_bar)

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)

        # Draw background of bar (gray)
        painter.setBrush(QColor(50, 50, 50, 200))
        painter.drawRect(self.bar_x, self.bar_y, self.bar_width, self.bar_height)

        # Draw actual bar (green)
        bar_fill_width = int((self.bar_value / 100) * self.bar_width)
        painter.setBrush(QColor(0, 255, 0, 200))
        painter.drawRect(self.bar_x, self.bar_y, bar_fill_width, self.bar_height)

    def drain_bar(self, event=None):
        """Drains the bar when 'F' is pressed."""
        if self.bar_value > 0:
            self.bar_value = max(0, self.bar_value - self.bar_decrease_amount)
            self.update()

    def refill_bar(self):
        """Refills the bar over time."""
        if self.bar_value < 100:
            self.bar_value = min(100, self.bar_value + self.bar_refill_speed)
            self.update()

# Global variable to track the overlay instance
overlay_instance = None

def overlay():
    """Toggles the overlay on/off when called."""
    global overlay_instance
    if overlay_instance is None:
        overlay_instance = Overlay()
    else:
        overlay_instance.close()
        overlay_instance = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay()  # Start with overlay on
    sys.exit(app.exec_())
