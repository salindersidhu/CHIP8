#Python CHIP-8 Interpreter

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
ROMs for the CHIP-8 system can be downloaded for free at [Chip8.com](http://www.chip8.com/?page=84) and [Zophar's Domain](http://www.zophar.net/pdroms/chip8.html). In order to load these ROMs with the interpreter, the files must be renamed to have a `.c8` extension.

Dependencies:
-------------
- `Python 3` [(Build 3.4)](https://www.python.org/downloads/)
- `PyQt 4` [(Build 4.11)](https://riverbankcomputing.com/software/pyqt/download)

Running the Interpreter:
-------------
1. Clone the repo to obtain the source code
2. Download and install `Python3`
3. Download and install `PyQt 4`
4. Open a `command prompt` or `console` and navigate to the cloned repo's directory using the `cd` command
5. Run the following command, `python interpreterapp.py` to launch the interpreter GUI
6. Load a ROM to test the interpreter, ensure that the ROM file has a `.c8` extension

Controls:
-------------
The CHIP-8 system uses a `hexadecimal keyboard` that has 16 keys from 0 to 9 and A to F. Keys `2`, `4`, `6` and `8` are typically used for directional input.

The following keyboard layouts specify the `CHIP-8 Keyboard` and the `Interpreter Keybinds` used in the application.

<table>
	<caption>CHIP-8 Keyboard</caption>
	<tr>
		<td><b>1</b></td>
		<td><b>2</b></td>
		<td><b>3</b></td>
		<td><b>C</b></td>
	</tr>
	<tr>
		<td><b>4</b></td>
		<td><b>5</b></td>
		<td><b>6</b></td>
		<td><b>D</b></td>
	</tr>
	<tr>
		<td><b>7</b></td>
		<td><b>8</b></td>
		<td><b>9</b></td>
		<td><b>E</b></td>
	</tr>
	<tr>
		<td><b>A</b></td>
		<td><b>0</b></td>
		<td><b>B</b></td>
		<td><b>F</b></td>
	</tr>
</table>
<table>
	<caption>Interpreter Keybinds</caption>
	<tr>
		<td><b>1</b></td>
		<td><b>2</b></td>
		<td><b>3</b></td>
		<td><b>C</b></td>
	</tr>
	<tr>
		<td><b>Q</b></td>
		<td><b>W</b></td>
		<td><b>E</b></td>
		<td><b>R</b></td>
	</tr>
	<tr>
		<td><b>A</b></td>
		<td><b>S</b></td>
		<td><b>D</b></td>
		<td><b>F</b></td>
	</tr>
	<tr>
		<td><b>Z</b></td>
		<td><b>X</b></td>
		<td><b>C</b></td>
		<td><b>V</b></td>
	</tr>
</table>

License:
-------------
Copyright (c) 2015 Salinder Sidhu

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
