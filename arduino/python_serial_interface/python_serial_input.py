#!/usr/bin/env python3

import serial

arduino_serial = serial.Serial('/dev/ttyACM0', 9600)


while True:
    user_input = input()

    print(int(user_input))

    arduino_serial.write(bytes(user_input + "\r\n", 'utf-8'))
    # arduino_serial.flush()
