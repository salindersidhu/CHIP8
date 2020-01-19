# Python CHIP-8 Interpreter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](/LICENSE.md)

# Table of Contents

- [Overview](#overview)
  - [Features](#features)
  - [Supported Platforms](#supported-platforms)
  - [ROMs](#roms)
- [Development](#development)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
  - [Running](#running)
  - [Controls](#controls)
  - [Contributing](#contributing)
- [Codebase](#codebase)
  - [Structure](#structure)

## Overview:

A Python based GUI implementation of the CHIP-8 system. A project I developed with the intention of gaining knowledge about emulators and cross platform GUI libraries.
For more specific information about the CHIP-8 system, please refer to the following technical reference article on [CHIP-8](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM) and the [WIKI](https://en.wikipedia.org/wiki/CHIP-8).

## Features:

- Implementation of all 35 CHIP-8 opcodes
- Custom pixel and background colour rendering
- Saving and loading of emulation state
- Sound effects

## Supported Platforms:

- Windows 10, Mac OS X and Linux based distributions

## ROMs:

ROMs for the CHIP-8 system can be obtained online for free at [Internet Archive](https://archive.org/details/Chip-8RomsThatAreInThePublicDomain). In order to load these ROMs with the interpreter, the files must be renamed to have a `.c8` extension.

# Development

> Information describing how to install and configure all the required tools to begin development.

## Prerequisites:

Ensure that you have the following installed and configured any environment variables.

- **Python**
  - Version 3.7.5+

## Setup:

You will need to setup a python virtual environment and install the project's dependencies.

1. Skip this step if you're using Windows. If you're using Mac or Linux, you may need to install `pip` and `virtualenv` first:

```bash
sudo apt-get install python3-pip
sudo pip3 install virtualenv
```

2. Navigate to your CHIP-8 repo and create a new virtual environment with the following command:

```bash
# Windows
python -m venv venv

# Mac or Linux
virtualenv venv
```

3. Enable your virtual environment with the following command:

```bash
# Windows
source venv/Scripts/activate

# Mac or Linux
source venv/bin/activate
```

Your command line will be prefixed with `(venv)` which indicates that the virtual environment is enabled.

4. Install the project's dependencies with the following command:

```bash
pip install -r requirements.txt
```

## Running:

1. Enable your virtual environment with the following command:

```bash
# Windows
source venv/Scripts/activate

# Mac or Linux
source venv/bin/activate
```

2. Launch the CHIP-8 interpreter app with the following command:

```bash
python interpreterapp.py
```

## Controls:

The CHIP-8 system uses a `hexadecimal keyboard` that has 16 keys from 0 to 9 and A to F. Keys `2`, `4`, `6` and `8` are typically used for directional input.

The following keyboard layouts specify the `CHIP-8 Keyboard` and the `Interpreter KeyBoard` used in the application.

<p align='center'>
	<img src='https://user-images.githubusercontent.com/12175684/40276007-26e1efd6-5bcd-11e8-8e4b-b615659797ee.png' alt='Keyboard'/>
</p>

## Contributing

CHIP-8 welcomes contributions from anyone and everyone. Please see our [contributing guide](/CONTRIBUTING.md) for more info.

# Codebase

> Information describing the software architecture and how to maintain it while adding additional functionality.

## Structure

    .
    ├── ...
    ├── assets                      # Assets
    │    ├── icon.svg               # CHIP-8 interpreter window icon
    │    └── ...
    ├── chip8                       # CHIP-8 Python package
    │   ├── __init__.py             # Package init file
    │   ├── chip8.py                # CHIP-8 CPU logic
    │   ├── stack.py                # Stack data structure
    │   └── ...
    ├── gridframe.py                # PyQt5 frame for rending the CHIP-8 display
    ├── guiwindow.py                # PyQt5 GUI window setup and config
    ├── interpreterapp.py           # Main application
    ├── requirements.txt            # Dependencies to install with pip
    └── ...
