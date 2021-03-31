from utils import detect_binaries, get_hardware, run, logger
from constants import DEFAULT_HDMI, DEFAULT_AXIS, DEFAULT_THRESHOLD, \
    DEFAUT_POINTER, PROP_NAME, INTERVAL, DEFAULT_ORIENTATION
from os import environ
from time import sleep

previous_rotation = None


def rotate(threshold: int, axis: str, monitor: str, pointer: str,
           orientation: str):
    """This function checks the value of one of the axis available on
    the accelerometer.

    If the value is more than then defined treshold then the screen is
    rotated as well as the pointer matrix.

    If no values are defined, default ones from constants.py will be used.
    """
    global previous_rotation
    cmd_monitor = ['xrandr', '--output', monitor, '--rotate']
    data = {}

    # Retrieve accelerometer object.
    dev = get_hardware()

    # Retrieve all the axis values.
    data['x'] = dev.acceleration[0]
    data['y'] = dev.acceleration[1]
    data['z'] = dev.acceleration[2]

    if data[axis] >= threshold:
        orientation = DEFAULT_ORIENTATION
        cmd_pointer = 'xinput set-prop "{}" "{}" 0 1 0 -1 0 1 0 0 1'.format(
            pointer, PROP_NAME)
        if previous_rotation != orientation:
            cmd_monitor.append(orientation)
            run(command=cmd_monitor)
            run(command=cmd_pointer, shell=True)
            previous_rotation = orientation
            logger.info('rotated to right')
    else:
        orientation = 'normal'
        cmd_pointer = 'xinput set-prop "{}" "{}" 1 0 0 0 1 0 0 0 1'.format(
            pointer, PROP_NAME)
        if previous_rotation != orientation:
            cmd_monitor.append(orientation)
            run(command=cmd_monitor)
            run(command=cmd_pointer, shell=True)
            previous_rotation = orientation
            logger.info('rotated to normal')


if __name__ == "__main__":
    # Check some requirements.
    detect_binaries()

    # Retrieve the information that will be used.
    interval = environ.get('INTERVAL', INTERVAL)
    threshold = environ.get('THRESHOLD', DEFAULT_THRESHOLD)
    axis = environ.get('AXIS', DEFAULT_AXIS)
    monitor = environ.get('MONITOR', DEFAULT_HDMI)
    pointer = environ.get('POINTER', DEFAUT_POINTER)
    orientation = environ.get('ORIENTATION', DEFAULT_ORIENTATION)

    # Check for the axis value at regular interval.
    while True:
        rotate(threshold=int(threshold),
               axis=axis,
               monitor=monitor,
               pointer=pointer,
               orientation=orientation)
        sleep(int(interval))
