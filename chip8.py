from stack import Stack
from binascii import hexlify
from random import randint, seed


class Chip8(object):
    '''Chip8 implements all opcode instructions for the CHIP-8 system. It also
    provides additional functionality for tasks such bas input handling, access
    to the graphics buffer for rendering and dynamic state loading.'''

    def __init__(self):
        '''Create a new CHIP-8 object.'''
        self.__pc = 0               # Program counter
        self.__I = 0                # Address register
        self.__opCode = 0           # Operation code (string)
        self.__timers = [0, 0]      # Timers [delay, sound]
        self.__gfx = [[]]           # 2D graphics buffer
        self.__key = []             # I/O key list
        self.__stk = Stack()        # Main stack
        self.__ram = []             # Main memory
        self.__V = []               # Registers
        # The font set, used to draw plaintext characters
        self.__fontSet = ['F0', '90', '90', '90', 'F0', '20', '60', '20', '20',
                          '70', 'F0', '10', 'F0', '80', 'F0', 'F0', '10', 'F0',
                          '10', 'F0', '90', '90', 'F0', '10', '10', 'F0', '80',
                          'F0', '10', 'F0', 'F0', '80', 'F0', '90', 'F0', 'F0',
                          '10', '20', '40', '40', 'F0', '90', 'F0', '90', 'F0',
                          'F0', '90', 'F0', '10', 'F0', 'F0', '90', 'F0', '90',
                          '90', 'E0', '90', 'E0', '90', 'E0', 'F0', '80', '80',
                          '80', 'F0', 'E0', '90', '90', '90', 'E0', 'F0', '80',
                          'F0', '80', 'F0', 'F0', '80', 'F0', '80', '80']
        # Opcode instruction jump tables
        self.__opCodeTable = {'0': self.__jump0NNN, '1': self.__inst1NNN,
                              '2': self.__inst2NNN, '3': self.__inst3XNN,
                              '4': self.__inst4XNN, '5': self.__inst5XY0,
                              '6': self.__inst6XNN, '7': self.__inst7XNN,
                              '8': self.__jump8NNN, '9': self.__inst9XY0,
                              'a': self.__instANNN, 'b': self.__instBNNN,
                              'c': self.__instCXNN, 'd': self.__instDXYN,
                              'e': self.__jumpENNN, 'f': self.__jumpFNNN}
        self.__table0NNN = {'e0': self.__inst00E0, 'ee': self.__inst00EE}
        self.__table8NNN = {'0': self.__inst8XY0, '1': self.__inst8XY1,
                            '2': self.__inst8XY2, '3': self.__inst8XY3,
                            '4': self.__inst8XY4, '5': self.__inst8XY5,
                            '6': self.__inst8XY6, '7': self.__inst8XY7,
                            'e': self.__inst8XYE}
        self.__tableENNN = {'9e': self.__instEX9E, 'a1': self.__instEXA1}
        self.__tableFNNN = {'07': self.__instFX07, '0a': self.__instFX0A,
                            '15': self.__instFX15, '18': self.__instFX18,
                            '1e': self.__instFX18, '1e': self.__instFX1E,
                            '29': self.__instFX29, '33': self.__instFX33,
                            '55': self.__instFX55, '65': self.__instFX65}

    def reset(self):
        '''Reset the CHIP-8 system to it's original state. Clear all registers,
        graphics buffers, key mappings, timers, RAM buffer, stack and program
        counter. Load the default fontset.'''
        self.__pc = 512
        self.__I = 0
        self.__opCode = 0
        self.__timers = [0, 0]
        self.__gfx = [[0 for x in range(32)] for y in range(64)]
        self.__key = [0 for x in range(16)]
        self.__V = [0 for x in range(16)]
        self.__stk.clear()
        self.__ram = ['00' for x in range(4096)]
        # Load default fontset into memory
        for i in range(80):
            self.__ram[i] = self.__fontSet[i]

    def setKeyState(self, key, state):
        '''Set the state of a key.'''
        # Check if key list has been initialized
        if self.__key:
            self.__key[key] = state

    def getSoundTimer(self):
        '''Return the value of the sound timer.'''
        return self.__timers[1]

    def getGFX(self):
        '''Return the graphics buffer.'''
        # Check if the graphics buffer has been initialized
        if self.__gfx:
            return self.__gfx

    def getState(self):
        '''Return the state of the system.'''
        stateData = {
            'PRC': self.__pc,
            'ADR': self.__I,
            'OPC': self.__opCode,
            'TIM': self.__timers,
            'GFX': self.__gfx,
            'KEY': self.__key,
            'REG': self.__V,
            'STK': self.__stk,
            'RAM': self.__ram
        }
        return stateData

    def setState(self, stateData):
        '''Set the state of the system.'''
        self.__pc = stateData['PRC']
        self.__I = stateData['ADR']
        self.__opCode = stateData['OPC']
        self.__timers = stateData['TIM']
        self.__gfx = stateData['GFX']
        self.__key = stateData['KEY']
        self.__V = stateData['REG']
        self.__stk = stateData['STK']
        self.__ram = stateData['RAM']

    def loadROM(self, filename):
        '''Load a file's binary data into the system's RAM buffer.'''
        self.reset()
        # Load data from file in binary mode
        fileBuffer = open(filename, 'rb')
        romData = fileBuffer.read()
        fileBuffer.close()
        # Convert file data into hex
        hexData = str(hexlify(romData))[2:]  # Remove 'b from string
        # Pad string such that its length is a multiple of 4
        for i in range(len(hexData) % 4):
            hexData += '0'
        # Copy padded string into memory, each byte is 2 hex chars
        for i in range(0, len(hexData) - 1, 2):
            self.__ram[int(i / 2) + 512] = hexData[i:i + 2]

    def emulateCycle(self):
        '''Emulate a system cycle. Fetch the next instruction from RAM, decode
        the instruction using the opcode table and execute the instruction.'''
        # Fetch opcode
        self.__opCode = self.__ram[self.__pc] + self.__ram[self.__pc + 1]
        # Execute opcode function from table
        self.__opCodeTable[self.__opCode[0]]()
        # Update timers
        for i in range(len(self.__timers)):
            if self.__timers[i] > 0:
                self.__timers[i] -= 1

    def __jump0NNN(self):
        '''Opcode jump function for table0NNN.'''
        self.__table0NNN[self.__opCode[2:4]]()

    def __jump8NNN(self):
        '''Opcode jump function for table8NNN.'''
        self.__table8NNN[self.__opCode[3]]()

    def __jumpENNN(self):
        '''Opcode jump function for tableENNN.'''
        self.__tableENNN[self.__opCode[2:4]]()

    def __jumpFNNN(self):
        '''Opcode jump function for tableFNNN.'''
        self.__tableFNNN[self.__opCode[2:4]]()

    def __inst00E0(self):
        '''0x00E0: Clear the graphics buffer.'''
        self.__gfx = [[0 for x in range(32)] for y in range(64)]
        self.__pc += 2

    def __inst00EE(self):
        '''00EE: Return from subroutine.'''
        self.__pc = self.__stk.pop()
        self.__pc += 2

    def __inst1NNN(self):
        '''1NNN: Jump to address NNN.'''
        self.__pc = int(self.__opCode[1:4], 16)

    def __inst2NNN(self):
        '''2NNN: Call subroutine at NNN.'''
        self.__stk.push(self.__pc)
        self.__pc = int(self.__opCode[1:4], 16)

    def __inst3XNN(self):
        '''3XNN: Skip the next instruction if VX equals NN.'''
        if self.__V[int(self.__opCode[1], 16)] == int(self.__opCode[2:4], 16):
            self.__pc += 4
        else:
            self.__pc += 2

    def __inst4XNN(self):
        '''4XNN: Skip the next instruction if VX doesn't equal NN.'''
        if self.__V[int(self.__opCode[1], 16)] != int(self.__opCode[2:4], 16):
            self.__pc += 4
        else:
            self.__pc += 2

    def __inst5XY0(self):
        '''5XY0: Skip the next instruction if VX equals VY.'''
        if self.__V[int(self.__opCode[1], 16)] == \
           self.__V[int(self.__opCode[2], 16)]:
            self.__pc += 4
        else:
            self.__pc += 2

    def __inst6XNN(self):
        '''6XNN: Set VX to NN.'''
        self.__V[int(self.__opCode[1], 16)] = int(self.__opCode[2:4], 16)
        self.__pc += 2

    def __inst7XNN(self):
        '''7XNN: Add NN to VX.'''
        self.__V[int(self.__opCode[1], 16)] += int(self.__opCode[2:4], 16)
        self.__V[int(self.__opCode[1], 16)] &= 255  # Take the lowest 8 bits
        self.__pc += 2

    def __inst8XY0(self):
        '''8XY0: Set VX to the value of VY.'''
        self.__V[int(self.__opCode[1], 16)] = \
            self.__V[int(self.__opCode[2], 16)]
        self.__pc += 2

    def __inst8XY1(self):
        '''8XY1: Set VX to VX OR VY.'''
        self.__V[int(self.__opCode[1], 16)] |= \
            self.__V[int(self.__opCode[2], 16)]
        self.__pc += 2

    def __inst8XY2(self):
        '''8XY2: Set VX to VX AND VY.'''
        self.__V[int(self.__opCode[1], 16)] &= \
            self.__V[int(self.__opCode[2], 16)]
        self.__pc += 2

    def __inst8XY3(self):
        '''8XY3: Set VX to VX XOR VY.'''
        self.__V[int(self.__opCode[1], 16)] ^= \
            self.__V[int(self.__opCode[2], 16)]
        self.__pc += 2

    def __inst8XY4(self):
        '''8XY4: Add VY to VX. VF is set to 1 when there's a carry, and to 0
        when there isn't.'''
        self.__V[int(self.__opCode[1], 16)] += \
            self.__V[int(self.__opCode[2], 16)]
        if self.__V[int(self.__opCode[1], 16)] > 255:
            self.__V[15] = 1
            self.__V[int(self.__opCode[1], 16)] &= 255  # Take lowest 8 bits
        else:
            self.__V[15] = 0
        self.__pc += 2

    def __inst8XY5(self):
        '''8XY5: Subtract VY from VX. VF is set to 0 when there's a borrow, and
        1 when there isn't.'''
        if self.__V[int(self.__opCode[1], 16)] > \
           self.__V[int(self.__opCode[2], 16)]:
            self.__V[15] = 1
        else:
            self.__V[15] = 0  # There is a borrow
        self.__V[int(self.__opCode[1], 16)] -= \
            self.__V[int(self.__opCode[2], 16)]
        self.__pc += 2

    def __inst8XY6(self):
        '''8XY6: Shift VX right by 1. VF is set to the value of the least
        significant bit of VX before the shift.'''
        # Make binary string from integer
        binStr = bin(self.__V[int(self.__opCode[1], 16)])
        # Check for least significant bit
        if binStr[len(binStr)-1] == '1':
            self.__V[15] = 1
        elif binStr[len(binStr)-1] == '0':
            self.__V[15] = 0
        # Divide Vx by 2 by shifting right by 1
        self.__V[int(self.__opCode[1], 16)] >>= 1
        self.__pc += 2

    def __inst8XY7(self):
        '''8XY7: Set VX to VY minus VX. VF is set to 0 when there's a borrow,
        and 1 when there isn't.'''
        if self.__V[int(self.__opCode[2], 16)] > \
           self.__V[int(self.__opCode[1], 16)]:
            self.__V[15] = 1
        else:
            self.__V[15] = 0
        self.__V[int(self.__opCode[1], 16)] = \
            self.__V[int(self.__opCode[2], 16)] - \
            self.__V[int(self.__opCode[1], 16)]
        self.__pc += 2

    def __inst8XYE(self):
        '''8XYE: Shift VX left by one. VF is set to the value of the most
        significant bit of VX before the shift.'''
        # Check for least significant bit
        if int(self.__V[int(self.__opCode[1], 16)] / 255) > 1:
            self.__V[15] = 1
        else:
            self.__V[15] = 0
        self.__V[int(self.__opCode[1], 16)] = \
            (self.__V[int(self.__opCode[1], 16)] << 1) & 255
        self.__pc += 2

    def __inst9XY0(self):
        '''9XY0: Skip the next instruction if VX doesn't equal VY.'''
        if self.__V[int(self.__opCode[1], 16)] != \
           self.__V[int(self.__opCode[2], 16)]:
            self.__pc += 4
        else:
            self.__pc += 2

    def __instANNN(self):
        '''ANNN: Set I to the address NNN.'''
        self.__I = int(self.__opCode[1:4], 16)
        self.__pc += 2

    def __instBNNN(self):
        '''BNNN: Jump to the address NNN plus V0.'''
        self.__pc = int(self.__opCode[1:4], 16) + self.__V[0]

    def __instCXNN(self):
        '''CXNN: Set VX to a random number and NN.'''
        seed()
        self.__V[int(self.__opCode[1], 16)] = \
            (randint(0, 255) & int(self.__opCode[2:4], 16))
        self.__pc += 2

    def __instDXYN(self):
        '''DXYN: Draw a sprite at coordinate (VX, VY) that has a width of 8
        pixels and a height of N pixels. Each row of 8 pixels is read as
        bit-coded starting from memory location I value doesn't change after
        the execution of this instruction. VF is set to 1 if any screen pixels
        are flipped from set to unset when the sprite is drawn, and to 0 if
        that does not occur.'''
        x = self.__V[int(self.__opCode[1], 16)]
        y = self.__V[int(self.__opCode[2], 16)]
        length = int(self.__opCode[3], 16)
        self.__V[15] = 0
        data = []  # Hold data to be written to screen
        # Adjust data
        for i in range(length):
            data.append(bin(int(self.__ram[self.__I + i], 16)))
            data[i] = data[i].replace('0', '', 1)
            data[i] = data[i].replace('b', '', 1)
            # Pad the data so it's 8 chars long
            while len(data[i]) < 8:
                data[i] = '0' + data[i]
        # Drawing system
        for i in range(len(data)):
            for j in range(8):
                newX = x + j
                newY = y
                # Wrap to other side horizontally
                while newX >= 64:
                    newX -= 64
                # Wrap to other side vertically
                while newY >= 32:
                    newY -= 32
                # XOR drawing mode
                pxVal = int(data[i][j])
                if pxVal:
                    self.__gfx[newX][newY] = pxVal ^ self.__gfx[newX][newY]
                    if not self.__gfx[newX][newY]:
                        self.__V[15] = 1
            y += 1  # Move down to draw the next row
        self.__pc += 2

    def __instEX9E(self):
        '''EX9E: Skip the next instruction if the key stored in VX is
        pressed.'''
        if self.__key[self.__V[int(self.__opCode[1], 16)]]:
            self.__pc += 4
        else:
            self.__pc += 2

    def __instEXA1(self):
        '''EXA1 Skip the next instruction if the key stored in VX is not
        pressed.'''
        if not self.__key[self.__V[int(self.__opCode[1], 16)]]:
            self.__pc += 4
        else:
            self.__pc += 2

    def __instFX07(self):
        '''FX07: Set VX to the value of the delay timer.'''
        self.__V[int(self.__opCode[1], 16)] = self.__timers[0]
        self.__pc += 2

    def __instFX0A(self):
        '''FX0A: Wait for a key press and stored the key in VX.'''
        isKeyPressed = False
        for i in range(16):
            if self.__key[i]:
                self.__V[int(self.__opCode[1], 16)] = i
            isKeyPressed = True
        # If no key pressed, skip this cycle.
        if not isKeyPressed:
            return
        self.__pc += 2

    def __instFX15(self):
        '''FX15: Set the delay timer to VX.'''
        self.__timers[0] = self.__V[int(self.__opCode[1], 16)]
        self.__pc += 2

    def __instFX18(self):
        '''FX18: Set the sound timer to VX.'''
        self.__timers[1] = self.__V[int(self.__opCode[1], 16)]
        self.__pc += 2

    def __instFX1E(self):
        '''FX1E: Add VX to I.'''
        self.__I += self.__V[int(self.__opCode[1], 16)]
        self.__pc += 2

    def __instFX29(self):
        '''FX29: Set I to the location of the sprite for the character in
        VX.'''
        self.__I = (self.__V[int(self.__opCode[1], 16)] * 5)
        self.__pc += 2

    def __instFX33(self):
        '''FX33: Store the Binary-coded decimal representation of VX at the
        addresses I, I plus 1, and I plus 2.'''
        num = self.__V[int(self.__opCode[1], 16)]
        self.__ram[self.__I] = hex(int(num / 100)).replace('x', '')
        num -= 100 * int(num / 100)
        self.__ram[self.__I + 1] = hex(int(num / 10)).replace('x', '')
        num -= 10 * int(num / 10)
        self.__ram[self.__I + 2] = hex(num).replace('x', '')
        self.__pc += 2

    def __instFX55(self):
        '''FX55: Store V0 to VX in memory starting at address I.'''
        for i in range(int(self.__opCode[1], 16) + 1):
            self.__ram[self.__I + i] = hex(self.__V[i]).replace('x', '')
        self.__pc += 2

    def __instFX65(self):
        '''FX65: Fill V0 to VX with values from memory starting at address
        I.'''
        for i in range(int(self.__opCode[1], 16) + 1):
            self.__V[i] = int(self.__ram[self.__I + i], 16)
        self.__pc += 2
