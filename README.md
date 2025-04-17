# BQ25895
BQ25895 - Home Assistant custom integration to communicate with Texas Instruments BQ25895 I2C Controlled Single Cell 5-A Fast Charger.

[BQ25895 Datasheet](http://www.ti.com/lit/ds/symlink/bq25895.pdf)

![icon](https://github.com/user-attachments/assets/3f028687-c074-4f35-959f-4629022dd84e)

## Installation

### HACS

If you use [HACS](https://hacs.xyz/) you can install and update this component.

1. Go into HACS -> CUSTOM REPOSITORIES and add url: <https://github.com/DJTerentjev/bq25895> with type "integration"
2. Go to integration, search "bq25895" and click Install.

### Manual

Download and unzip or clone this repository and copy content of `custom_components/bq25895/` to your configuration directory of Home Assistant, e.g. `~/.homeassistant/custom_components/bq25895/`.

In the end your file structure should look like that:

```
~/.homeassistant/custom_components/bq25895/__init__.py
~/.homeassistant/custom_components/bq25895/manifest.json
~/.homeassistant/custom_components/bq25895/const.py
~/.homeassistant/custom_components/bq25895/bq25895/bq25895.py
```
