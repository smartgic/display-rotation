#!/usr/bin/env python

import subprocess
import os
import board
import busio

from adafruit_adxl34x import ADXL345
from time import sleep

last_orientation = "normal"
touch_name = "Touch p303 Touch Device,99-20P"
matrix_name = "Coordinate Transformation Matrix"


def orientation(threshold: int = 10, axis: str = "x",
                touchscreen: str = touch_name, matrix: str = matrix_name):

    global last_orientation

    try:
        data = {}
        data["x"] = adxl.acceleration[0]
        data["y"] = adxl.acceleration[1]
        data["z"] = adxl.acceleration[2]

        cmd_display = ["xrandr", "--output", "HDMI-1", "--rotate"]

        if data[axis] >= threshold:
            if last_orientation != "right":

                cmd_display.append("right")
                display_process = subprocess.Popen(cmd_display,
                                                   stdout=subprocess.PIPE,
                                                   stderr=subprocess.STDOUT)
                cmd_touch = [
                    f'xinput set-prop "{touchscreen}" "{matrix_name}" 0 1 0 -1 0 1 0 0 1']

                touch_process = subprocess.Popen(cmd_touch, shell=True,
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.STDOUT)

                last_orientation = "right"

                return display_process.communicate(), touch_process.communicate()

        else:
            if last_orientation != "normal":
                cmd_display.append("normal")
                display_process = subprocess.Popen(cmd_display,
                                                   stdout=subprocess.PIPE,
                                                   stderr=subprocess.STDOUT)

                cmd_touch = [
                    f'xinput set-prop "{touchscreen}" "{matrix_name}" 1 0 0 0 1 0 0 0 1']

                touch_process = subprocess.Popen(cmd_touch, shell=True,
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.STDOUT)

                last_orientation = "normal"

                return display_process.communicate(), touch_process.communicate()

    except RuntimeError as e:
        return e.args[0]
    except Exception as e:
        raise e


if __name__ == "__main__":
    i2c = busio.I2C(board.SCL, board.SDA)
    adxl = ADXL345(i2c)

    while True:
        orientation()
        sleep(1)
