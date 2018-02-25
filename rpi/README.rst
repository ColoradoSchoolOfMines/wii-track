Python Applications
================================================

pygame_camera_capture.py
------------------------
    * Captures camera data (from /dev/video0) and renders it to a pygame surface
    * Extracts PNG data to be send to AWS lambda for processing

python_qt_serial_gui.py
-----------------------
    * Creates a PyQT5 gui with a slider that allows controlling the servo angle
    * Controls the servo by sending values from 0-180 over the serial interface
    * Displays camera output by copying pygame surface to QtPixmap
    * Can upload image to database, base64 encoded

python_serial_input.py
----------------------
    * Basic python cli application that mirrors the sending functionality of the python IDE's serial monitor
