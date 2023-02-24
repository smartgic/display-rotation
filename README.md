[![Docker pulls](https://img.shields.io/docker/pulls/smartgic/display-rotation.svg?style=flat&logo=docker&logoColor=FFFFFF&color=87567)](https://hub.docker.com/r/smartgic/display-rotation) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-pink.svg?style=flat)](https://github.com/smartgic/display-rotation/pulls) [![Discord](https://img.shields.io/discord/809074036733902888)](https://discord.com/invite/sHM3Duz5d3)

# Display rotation

This application will rotate screen and pointer *(mouse, touchscreen, etc...)* based on an accelerometer axis values.

## Requirements

A X server is required. X applications such as `xrandr` *(rotate display)* and `xinput` *(rotate pointer)* are required too.

The code has been developped using the [ADXL345](https://amzn.to/3HGeOO9) accelerometer, I'll recommend any accelerometer compatible with the `adafruit-circuitpython-adxl34x` Python library. Have a look to the [Smart'Gic Abstract RPi API](https://github.com/smartgic/abstract-rpi).

<img src='https://cdn-learn.adafruit.com/assets/assets/000/006/359/medium800/adafruit_products_2013_03_24_IMG_1453-1024.jpg?1396835278' width='250'/>

Because this accelerometer is connected to an I2C bus, an I2C bus is required. The code has been developped for Raspberry Pi but should work for any other platforms supporting I2C bus and able to run Python code.

## Retrieve available monitors and pointers

`xrandr` will provide a list of available monitors/TV connected to your device.

```bash
xrandr --listmonitors
Monitors: 1
 0: +*HDMI-1 1080/1210x1920/680+0+0  HDMI-1
```

`xinput` will provide a list of available pointers *(mouse, touchscreen, etc...)* connected to your device.

```bash
xinput list
⎡ Virtual core pointer                    	id=2	[master pointer  (3)]
⎜   ↳ Virtual core XTEST pointer              	id=4	[slave  pointer  (2)]
⎜   ↳ Touch p303 Touch Device,99-20P Mouse    	id=7	[slave  pointer  (2)]
⎜   ↳ Touch p303 Touch Device,99-20P          	id=8	[slave  pointer  (2)]
⎣ Virtual core keyboard                   	id=3	[master keyboard (2)]
    ↳ Virtual core XTEST keyboard             	id=5	[slave  keyboard (3)]
    ↳ Touch p303 Touch Device,99-20P Keyboard 	id=6	[slave  keyboard (3)]
```

## Installation

Some environment variables should be defined to match your setup.

| Variables     | Description                                            | Default |
| ---           | ---                                                    | --- |
| `INTERVAL`    | Check the accelerometer every `iNTERVAL` *(in second)* | `1` |
| `THRESHOLD`   | Define when the axis reach a point of action           | `10` |
| `AXIS`        | Which axis to check *(`x`, `y`, `z`)*                  | `x` |
| `MONITOR`     | Interface name where the monitor is connected          | `HDMI-1` |
| `POINTER`     | Name of the mouse, touchscreen, etc... to rotate       | `Touch p303 Touch Device,99-20P` |
| `ORIENTATION` | Direction where the monitor will be rorated            | `right` |

### Virtualenv installation

```bash
git clone https://github.com/smartgic/display-rotation.git
cd display-rotation
python3 -m venvs ~/venvs/display-rotation
source ~/venvs/display-rotation/bin/activate
pip install -r requirements.txt
cd app
export POINTER="Logitech M325"
python rotation.py
```

### Docker installation

Supported architectures for Docker `smartgic/display-rotation` image.

| Architecture | Information                                        |
| ---          | ---                                                |
| `amd64`      | Such as AMD and Intel processors                   |
| `arm/v6`     | Such as Raspberry Pi 1                             |
| `arm/v7`     | Such as Raspberry Pi 2/3/4                         |
| `arm64`      | Such as Raspberry Pi 4 64-bit                      |
| `ppc64`      | Such as PowerPC 64 platforms                       |


The container needs to be authenticated to access the X Server and run the GUI. One way to do it is to use `xauth` *(part of the `xauth` package on Debian/Ubuntu)* which will generate a X authentication token. This token will have to be mounted as a volume within the container to be then used via the `XAUTHORITY` environment variable.

```bash
$ touch ~/.docker.xauth
$ xauth nlist :0 | sed -e 's/^..../ffff/' | xauth -f ~/.docker.xauth nmerge -
```

```bash
docker run -d \
    --volume /sys:/sys:ro \
    --volume /tmp/.X11-unix:/tmp/.X11-unix \
    --volume ~/.docker.xauth:/tmp/.docker.xauth:ro \
    --device /dev/i2c-1 \
    --env DISPLAY=:0 \
    --env XAUTHORITY=/tmp/.docker.xauth \
    --env THRESHOLD=10 \
    --env AXIS=x \
    --env MONITOR=HDMI-1 \
    --env POINTER="Logitech M325" \
    --env INTERVAL=1 \
    --env ORIENTATION=right \
    --name display_rotation \
    smartgic/display-rotation:latest
```

`/dev/i2c-1` could change depending the hardware used *(`i2c` from Raspberry Pi 4B)*.

### Docker Compose installation

Make sure `docker-compose` is installed if not use your package manager or `pip`.

```bash
git clone https://github.com/smartgic/display-rotation.git
cd display-rotation
docker-compose up -d
```

## Credits

Developed by [Smart"Gic](https://smartgic.io).
