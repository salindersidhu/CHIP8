#Python CHIP-8 CPU Interpreter

Description:
-------------
A Python based GUI implementation of the CHIP-8 system. A project I developed with the intention of gaining knowledge about emulators and cross platform GUI libraries.
For more specific information about the CHIP-8 system, please refer to the following WIKI article on [CHIP-8](https://en.wikipedia.org/wiki/CHIP-8).

Supports:
-------------
- Microsoft Windows 7, 8, 8.1, 10
- Linux Based Distributions

ROMs:
-------------
ROMs for the CHIP-8 system can be downloaded for free at [Chip8.com](http://www.chip8.com/?page=84) and [Zophar's Domain](http://www.zophar.net/pdroms/chip8.html). In order to load these ROMs with the emulator, the files must be renamed to have a `.c8` extension.

Dependencies:
-------------
- `Python 3` [(Build 3.4)](https://www.python.org/downloads/)
- `PyQt 4` [(Build 4.11)](https://riverbankcomputing.com/software/pyqt/download)

Running the Emulator:
-------------
1. Clone the repo to obtain the source code
2. Download and install `Python3`
3. Download and install `PyQt 4`
4. Open a `command prompt` or `console` and navigate to the cloned repo directory using the `cd` command
5. Run the following command, `python emulator.py` to launch the emulator GUI
6. Load a ROM to test the emulator, ensure that the ROM file has a `.c8` extension

Controls:
-------------
The CHIP-8 system uses a `hexadecimal keyboard` that has 16 keys ranging from 0 to 9 and A to F. Keys `2`, `4`, `6` and `8` are typically used for directional input.

The following keyboard layouts specify the `CHIP-8 Keyboard` and the `Default Keybinds` used in the emulator. The key binding settings can be changed through the `settings` menu.

CHIP-8 Keyboard Map
1 | 2 | 3 | C
:-: | :-: | :-: | :-:
**4** | **5** | **6** | **D**
**7** | **8** | **9** | **E**
**A** | **0** | **B** | **F**

Default Emulator Keybinds
1 | 2 | 3 | 4
:-: | :-: | :-: | :-:
**Q** | **W** | **E** | **R**
**A** | **S** | **D** | **F**
**Z** | **X** | **C** | **V**

License:
-------------
Copyright (c) 2015 Salinder Sidhu

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
