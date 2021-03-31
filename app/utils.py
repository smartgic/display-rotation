"""This file contains functions that could be used multiple times
"""
from busio import I2C
from adafruit_adxl34x import ADXL345
from constants import XINPUT_BINARY, XRANDR_BINARY
from distutils.spawn import find_executable
import board
import subprocess as proc


def get_hardware():
    """Retrieve accelerometer fom I2C bus.
    """
    try:
        # board is part of adafruit-blinka and helps to manage
        # defferent type of boards.
        i2c = I2C(board.SCL, board.SDA)

        # If an I2C device is detected then we check if it's an
        # accelerometer usable by ADXL345 library.
        if len(i2c.scan()) > 0:
            try:
                return ADXL345(i2c)
            except Exception as err:
                print('accelerometer not found. {}'.format(err))
        else:
            print('no i2c devices found')
    except Exception as err:
        print('i2c bus not found, check your hardware {}'.format(err))


def detect_binaries():
    """Make sure xrandr and xinput binaries are available.
    """
    try:
        for binary in XINPUT_BINARY, XRANDR_BINARY:
            if find_executable(binary) is None:
                print('{} binary not found'.format(binary))
    except Exception as err:
        print(err)


def run(command: list, shell: bool = False):
    """Simple wrapper for subprocess.run() command which allows
    to execute command as a list or as "pure" shell.

    If shell is True then the command variable will not be a list
    With shell = False: ['ps', 'faux']
    With shell = True: 'ps faux'
    """
    try:
        execution = None
        if shell:
            execution = proc.run(command,
                                 capture_output=True,
                                 text=True,
                                 shell=True)
        else:
            execution = proc.run(command,
                                 capture_output=True,
                                 text=True)
        execution.check_returncode()
        print(execution.stdout)
    except proc.CalledProcessError as err:
        print(err)
