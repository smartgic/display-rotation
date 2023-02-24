"""This file contains functions that could be used multiple times
"""
import subprocess as proc
import logging
import sys
from distutils.spawn import find_executable
import json_logging
from busio import I2C
from adafruit_adxl34x import ADXL345
from constants import XINPUT_BINARY, XRANDR_BINARY
import board

# Logger setup, configured to return JSON.
json_logging.init_non_web(enable_json=True)
logger = logging.getLogger("display-rotation")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))


def get_hardware():
    """Retrieve accelerometer fom I2C bus."""
    try:
        # board is part of adafruit-blinka and helps to manage
        # defferent type of boards.
        i2c = I2C(board.SCL, board.SDA)

        # If an I2C device is detected then we check if it's an
        # accelerometer usable by ADXL345 library.
        if len(i2c.scan()) > 0:
            try:
                return ADXL345(i2c)
            except RuntimeError as err:
                logger.warning("accelerometer not found, error: %s", err)
                return None
        else:
            logger.warning("no i2c devices found")
    except RuntimeError as err:
        logger.error("i2c bus not found, check your hardware, error: %s", err)
        return None


def detect_binaries():
    """Make sure xrandr and xinput binaries are available."""
    try:
        for binary in XINPUT_BINARY, XRANDR_BINARY:
            if find_executable(binary) is None:
                logger.error("binary not found, error: %s", binary)
    except RuntimeError as err:
        logger.error(err)


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
            execution = proc.run(
                command, capture_output=True, text=True, shell=True, check=False
            )
        else:
            execution = proc.run(command, capture_output=True, text=True, check=False)
        execution.check_returncode()
        logger.debug(command)
        logger.info(execution.stdout)
    except proc.CalledProcessError as err:
        logger.error(err)
