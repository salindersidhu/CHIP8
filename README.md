# Python CHIP-8 Interpreter

[![Contributors](https://img.shields.io/github/contributors/salindersidhu/CHIP8?style=for-the-badge)](https://github.com/salindersidhu/CHIP8/graphs/contributors) [![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2Fsalindersidhu%2FCHIP8&countColor=%23263759)](https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2Fsalindersidhu%2FCHIP8) [![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=for-the-badge)](/LICENSE)

## Overview

A Python based GUI implementation of the CHIP-8 system. A project I developed with the intention of gaining knowledge about emulators and cross platform GUI libraries.
For more specific information about the CHIP-8 system, please refer to the following technical reference article on [CHIP-8](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM) and the [WIKI](https://en.wikipedia.org/wiki/CHIP-8). Built using Python and other open source technologies.

<p float="left">
    <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" height="150" width="150">
    <img src="https://pic4.zhimg.com/v2-f7c3d79d423db49691daaf3b78e3fb07_ipico.jpg" height="150" width="150">
</p>

## Features

<p float="center">
  <img src="https://user-images.githubusercontent.com/12175684/72684765-58b37600-3ab1-11ea-9b5c-9a9ea3b9d52c.gif" alt="screen capture"/>
</p>

- Implementation of all 35 CHIP-8 opcodes
- Custom pixel and background colours
- Saving and loading emulation state
- Sound effects

## Prerequisite Software

| Software       | Version   |
| :------------- | :-------- |
| Python         | 3.11+     |

### ROMs

ROMs for the CHIP-8 system can be obtained online for free at [Internet Archive](https://archive.org/details/Chip-8RomsThatAreInThePublicDomain).

## Getting Started

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

If you have recently pulled changes from a remote branch, you should re-run the above command to obtain any new dependencies that may have been added to the project.

## Running

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

### Controls

The CHIP-8 system uses a `hexadecimal keyboard` that has 16 keys from 0 to 9 and A to F. Keys `2`, `4`, `6` and `8` are typically used for directional input.

The following keyboard layouts specify the `CHIP-8 Keyboard` and the `Interpreter KeyBoard` used in the application.

<p align='center'>
	<img src='https://user-images.githubusercontent.com/12175684/40276007-26e1efd6-5bcd-11e8-8e4b-b615659797ee.png' alt='Keyboard'/>
</p>

## Contributing

Please see our [Contributing Guide](/CONTRIBUTING.md) for more info.

## Project Structure

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
