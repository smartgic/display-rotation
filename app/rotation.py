from os import environ
from time import sleep
from utils import detect_binaries, get_hardware, run, logger
from constants import (
    DEFAULT_HDMI,
    DEFAULT_AXIS,
    DEFAULT_THRESHOLD,
    DEFAUT_POINTER,
    PROP_NAME,
    INTERVAL,
    DEFAULT_ORIENTATION,
)

# This is used to avoid the execution of xrandr and xinput every INTERVAL.
PREVIOUS_ROTATION = None


def rotate(threshold: int, axis: str, monitor: str, pointer: str, way: str):
    """This function checks the value of one of the axis available on
    the accelerometer.

    If the value is more than then defined treshold then the screen is
    rotated as well as the pointer matrix.

    If no values are defined, default ones from constants.py will be used.
    """
    global PREVIOUS_ROTATION
    cmd_monitor = ["xrandr", "--output", monitor, "--rotate"]
    data = {}

    # Retrieve accelerometer object.
    dev = get_hardware()

    # Retrieve all the axis values.
    data["x"] = dev.acceleration[0]
    data["y"] = dev.acceleration[1]
    data["z"] = dev.acceleration[2]

    if data[axis] >= threshold:
        orientation = way
        cmd_pointer = f'xinput set-prop "{pointer}" "{PROP_NAME}" 0 1 0 -1 0 1 0 0 1'
        if PREVIOUS_ROTATION != orientation:
            cmd_monitor.append(orientation)
            run(command=cmd_monitor)
            run(command=cmd_pointer, shell=True)
            PREVIOUS_ROTATION = orientation
            logger.info("rotated to %s ", orientation)
    else:
        orientation = "normal"
        cmd_pointer = f'xinput set-prop "{pointer}" "{PROP_NAME}" 1 0 0 0 1 0 0 0 1'
        if PREVIOUS_ROTATION != orientation:
            cmd_monitor.append(orientation)
            run(command=cmd_monitor)
            run(command=cmd_pointer, shell=True)
            PREVIOUS_ROTATION = orientation
            logger.info("rotated to normal")


if __name__ == "__main__":
    # Check some requirements.
    detect_binaries()

    # Check for the axis value at regular interval.
    while True:
        rotate(
            threshold=int(environ.get("THRESHOLD", DEFAULT_THRESHOLD)),
            axis=environ.get("AXIS", DEFAULT_AXIS),
            monitor=environ.get("MONITOR", DEFAULT_HDMI),
            pointer=environ.get("POINTER", DEFAUT_POINTER),
            way=environ.get("ORIENTATION", DEFAULT_ORIENTATION),
        )
        sleep(int(environ.get("INTERVAL", INTERVAL)))
