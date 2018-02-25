#!/usr/bin/env python3

import serial
import sys
import time
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QSlider, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 simple window - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

        self.arduino_serial = serial.Serial('/dev/ttyACM0', 9600, timeout=0)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 40)

        # Create a button in the window
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.move(20, 80)
        self.slider.resize(280, 40)

        # connect button to function on_click
        self.slider.sliderReleased.connect(self.on_click)
        self.show()

    @pyqtSlot()
    def on_click(self):
        slider_value = self.slider.value()
        adjusted_value = slider_value * 179 / 99
        print(adjusted_value)
        self.arduino_serial.write(bytes(str(adjusted_value) + "\r\n", 'utf-8'))
        self.arduino_serial.flush()
        # time.sleep(0.1)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())









    # new_serial_data = arduino_serial.read(10000)
    # if new_serial_data:
    #     if b'\r\n' not in old_serial_data:
    #         old_serial_data += new_serial_data
    #     else:
    #         old_serial_data = new_serial_data
    # if b'\r\n' in old_serial_data and new_serial_data:
    #     print("      Serial: ", old_serial_data, end="\r")
