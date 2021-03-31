[![Build Status](https://travis-ci.com/smartgic/display-rotation.svg?branch=main)](https://travis-ci.com/github/smartgic/display-rotation) [![Python version](https://img.shields.io/badge/Python-3.9-green.svg?style=flat&logoColor=FFFFFF&color=87567)](https://hub.docker.com/_/python)
[![Docker pulls](https://img.shields.io/docker/pulls/smartgic/displau-rotation.svg?style=flat&logo=docker&logoColor=FFFFFF&color=87567)](https://hub.docker.com/r/smartgic/display-rotation) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-pink.svg?style=flat)](https://github.com/smartgic/display-rotation/pulls) [![Discord](https://img.shields.io/discord/809074036733902888)](https://discord.gg/Vu7Wmd9j)

# Display rotation

This application will rotate screen and pointer (mouse, touchscreen, etc...) based on an accelerometer axis value.

## Requirements

A X server is required. X applications such as `xrandr` *(rotate display)* and `xinput` *(rotate pointer)* are required too.

The code has been developped using the [!ADXL345](https://learn.adafruit.com/adxl345-digital-accelerometer) accelerometer, I'll recommend any accelerometer compatible with the `adafruit-circuitpython-adxl34x` Python library.

<img src='https://cdn-learn.adafruit.com/guides/cropped_images/000/000/247/medium640/2013_03_24_IMG_1453-1024.jpg?1520540491' width='250'/>

Because this accelerometer is connected to an I2C bus, an I2C bus is required. The code has been developped for Raspberry Pi but should work for any other platforms supporting I2C bus and able to run Python code.

## Installation

### Virtualenv installation

```bash
$ git clone https://github.com/smartgic/display-rotation.git
$ cd display-rotation
$ python3 -m venvs ~/venvs/display-rotation
$ source ~/venvs/display-rotation/bin/activate
$ pip install -r requirements.txt
$ cd app
$ python rotation.py
```

### Docker installation

Supported architectures for Docker `smartgic/display-rotation` image:

| Architecture |
| ---          |
| `amd64`      |
| `arm/v6`     |
| `arm/v7`     |
| `arm64`      |
| `ppc64`      |

```bash
$ docker run -d \
    --volume /sys:/sys:ro \
    --volume /tmp/.X11-unix:/tmp/.X11-unix \
    --device /dev/i2c-1 \
    --env DISPLAY=:0 \
    --env THRESHOLD=10 \
    --env AXIS=x \
    --env MONITOR=HDMI-1 \
    --env POINTER=Logitech M325 \
    --env INTERVAL=1 \
    --name display_rotation \
    smartgic/display-rotation:latest
```

`/dev/i2c-1` could change depending the hardware used.


### Docker Compose installation
```bash
$ git clone https://github.com/smartgic/display-rotation.git
$ cd display-rotation
$ docker-compose up -d
```