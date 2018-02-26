#!/usr/bin/env python3

import serial
import os
import sys
import time
import boto3
import json
import base64
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pygame
from pygame.locals import *
import pygame.camera


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'wii-track'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 700
        self.initUI()
        self.image = None

        self.arduino_serial = serial.Serial('/dev/ttyACM0', 9600, timeout=0)

        width = 640
        height = 700

        pygame.init()
        pygame.camera.init()
        self.cam = pygame.camera.Camera("/dev/video0", (640, 480))
        self.cam.start()
        self.windowSurfaceObj = pygame.Surface
        # set_mode((wdth, height), 1, 16)
        # pygame.display.set_caption('Camera')

        self.curr_time = QTime(00, 00, 00)

        self.timer = QTimer()
        self.timer.timeout.connect(self.get_new_camera_image)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.textbox = QLineEdit(self)
        self.textbox.move((self.width / 2) - 140, 20)
        self.textbox.resize(280, 40)
        self.textbox.setReadOnly(True)
        self.textbox.setAlignment(Qt.AlignCenter)
        self.textbox.setText("Current Angle: 90")

        self.textboxi = QLineEdit(self)
        self.textboxi.move(500, 0)
        self.textboxi.resize(40, 40)

        # Create a button in the window
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.move((self.width / 2) - 140, 80)
        self.slider.resize(280, 40)
        self.slider.setSliderPosition(50)

        self.label = QLabel(self)
        self.label.resize(640, 480)
        self.label.move(0, 200)

        self.start_button = QPushButton(self)
        self.start_button.resize(100, 30)
        self.start_button.move((self.width / 2) - 160, 120)
        self.start_button.setText("Start Video")
        self.start_button.clicked.connect(self.start_video_timer)

        self.stop_button = QPushButton(self)
        self.stop_button.resize(100, 30)
        self.stop_button.move((self.width / 2) + 60, 120)
        self.stop_button.setText("Stop Video")
        self.stop_button.clicked.connect(self.stop_video_timer)

        self.capture_button = QPushButton(self)
        self.capture_button.resize(100, 30)
        self.capture_button.move((self.width / 2) - 50, 120)
        self.capture_button.setText("📷 Shoot")
        self.capture_button.clicked.connect(self.capture_camera_image)

        # connect button to function on_click
        self.slider.sliderReleased.connect(self.on_click)

        self.show()

    @pyqtSlot()
    def on_click(self):
        slider_value = self.slider.value()
        adjusted_value = slider_value * 179 / 99
        print(int(adjusted_value))
        self.textbox.setText("Current Angle: " + str(int(adjusted_value)))
        self.arduino_serial.write(bytes(str(adjusted_value) + "\r\n", 'utf-8'))

        # self.show()

        # self.windowSurfaceObj.blit(camSurfaceObj, (0, 0))
        # pygame.display.update()

        # self.arduino_serial.flush()
        # time.sleep(0.1)

    @pyqtSlot()
    def get_new_camera_image(self):

        image = self.cam.get_image()

        # pygame.image.save(image, "cam.png")
        data = pygame.image.tostring(image, "RGBA")
        image =  QImage(data, 640, 480,  QImage.Format_ARGB32).rgbSwapped()
        q = QPixmap.fromImage(image)

        # q = QPixmap("cam.bmp")
        # q = QPixmap.fromImage(image)
        # q.loadFromData(pygame.image.tostring(image, "RGBA", ]False), "RGBA")
        # print(q.getPixmap())

        self.label.setPixmap(q)

    @pyqtSlot()
    def capture_camera_image(self):

        if self.textboxi.text() is False:
                return

        # if self.timer.isActive():
        image = self.cam.get_image()

        image = pygame.transform.scale(image, (150, 150))

        pygame.image.save(image, "captured_image.png")

        with open("captured_image.png", "rb") as image_file:
               encoded_string = base64.b64encode(image_file.read())

        r = requests.post("https://46mfsnafs3.execute-api.us-east-1.amazonaws.com/testing/hackcu_color", json={"image": encoded_string, "id": int(self.textboxi.text())})
        print("saving into")
        print(int(self.textboxi.text()))
        print(r)
           # print(r is None)


    @pyqtSlot()
    def start_video_timer(self):
        self.timer.start(10)

    @pyqtSlot()
    def stop_video_timer(self):
        self.timer.stop()


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
