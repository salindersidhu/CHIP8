from binascii import hexlify
from random import randint, seed


class Stack(object):
    '''Stack a FIFO data storage structure.'''

    def __init__(self):
        '''Create a new Stack data type.'''
        self.stk_pointer = []

    def clear(self):
        '''Clear the stack.'''
        self.stk_pointer = []

    def push(self, item):
        '''Push item to the top of the stack.'''
        self.stk_pointer.append(item)

    def pop(self):
        '''Pop the top item off the stack.'''
        return self.stk_pointer.pop()


class Chip8Cpu(object):

    def __init__(self):
        self.pc = 0 # Program counter
        self.I = 0 # General purpose register
        self.opcode = 0 # Operation code (string)
        self.timers = [0, 0] # Timers [delay, sound]
        self.draw_flag = True # Control when drawing should occur
        self.gfx = [[]] # 2D graphics list [x][y]
        self.key = [] # I/O key list
        self.stk = Stack()
        self.ram = [] # Main memory for CPU
        self.V = [] # Registers
        self.font_set = ["F0", "90", "90", "90", "F0",
                         "20", "60", "20", "20", "70",
                         "F0", "10", "F0", "80", "F0",
                         "F0", "10", "F0", "10", "F0",
                         "90", "90", "F0", "10", "10",
                         "F0", "80", "F0", "10", "F0",
                         "F0", "80", "F0", "90", "F0",
                         "F0", "10", "20", "40", "40",
                         "F0", "90", "F0", "90", "F0",
                         "F0", "90", "F0", "10", "F0",
                         "F0", "90", "F0", "90", "90",
                         "E0", "90", "E0", "90", "E0",
                         "F0", "80", "80", "80", "F0",
                         "E0", "90", "90", "90", "E0",
                         "F0", "80", "F0", "80", "F0",
                         "F0", "80", "F0", "80", "80"]
        # Opcode instruction jump tables
        self.opcode_table = {"0":self.inst_0x0NNN, "1":self.inst_0x1NNN,
                             "2":self.inst_0x2NNN, "3":self.inst_0x3XNN,
                             "4":self.inst_0x4XNN, "5":self.inst_0x5XY0,
                             "6":self.inst_0x6XNN, "7":self.inst_0x7XNN,
                             "8":self.inst_0x8NNN, "9":self.inst_0x9XY0,
                             "a":self.inst_0xANNN, "b":self.inst_0xBNNN,
                             "c":self.inst_0xCXNN, "d":self.inst_0xDXYN,
                             "e":self.inst_0xENNN, "f":self.inst_0xFNNN}
        self.table_0x0NNN = {"e0":self.inst_0x00E0, "ee":self.inst_0x00EE}
        self.table_0x8NNN = {"0":self.inst_0x8XY0, "1":self.inst_0x8XY1,
                             "2":self.inst_0x8XY2, "3":self.inst_0x8XY3,
                             "4":self.inst_0x8XY4, "5":self.inst_0x8XY5,
                             "6":self.inst_0x8XY6, "7":self.inst_0x8XY7,
                             "e":self.inst_0x8XYE}
        self.table_0xENNN = {"9e":self.inst_0xEX9E, "a1":self.inst_0xEXA1}
        self.table_0xFNNN = {"07":self.inst_0xFX07, "0a":self.inst_0xFX0A,
                             "15":self.inst_0xFX15, "18":self.inst_0xFX18,
                             "1e":self.inst_0xFX18, "1e":self.inst_0xFX1E,
                             "29":self.inst_0xFX29, "33":self.inst_0xFX33,
                             "55":self.inst_0xFX55, "65":self.inst_0xFX65}

    def _reset(self):
        # Reset CPU
        self.pc = 512
        self.I = 0
        self.opcode = 0
        self.timers = [0, 0]
        self.gfx = [[0 for x in range(32)] for y in range(64)]
        self.key = [0 for x in range(16)]
        self.V = [0 for x in range(16)]
        self.stk.clear()
        self.ram = ["00" for x in range(4096)]
        # Load fontset into memory
        for i in range(80):
            self.ram[i] = self.font_set[i]

    def load_rom(self, file_name):
        self._reset()
        # Load data from file in bin mode
        file_buffer = open(file_name, "rb")
        rom_data = file_buffer.read()
        file_buffer.close()
        # Convert file data into hex
        hex_data = hexlify(rom_data)
        # Pad string such that its length is a multiple of 4
        for i in range(len(hex_data) % 4):
            hex_data += "0"
        # Copy padded string into memory, each byte is 2 hex chars
        for i in range(0, len(hex_data) - 1, 2):
            self.ram[(i / 2) + 512] = hex_data[i:(i + 2)]

    def emulate_cycle(self):
        # Fetch opcode
        self.opcode = self.ram[self.pc] + self.ram[self.pc + 1]
        # Interpret opcode from table
        self.opcode_table[self.opcode[0]]()
        # Update timers
        for i in range(2):
            if self.timers[i] > 0:
                if self.timers[1] == 1:
                    pass#Beep(800, 100)
                self.timers[i] -= 1

    def inst_0x0NNN(self):
        '''Opcode jump function for table_0x0NNN.'''
        self.table_0x0NNN[self.opcode[2:4]]()

    def inst_0x8NNN(self):
        '''Opcode jump function for table_0x8NNN.'''
        self.table_0x8NNN[self.opcode[3]]()

    def inst_0xENNN(self):
        '''Opcode jump function for table_0xENNN.'''
        self.table_0xENNN[self.opcode[2:4]]()

    def inst_0xFNNN(self):
        '''Opcode jump function for table_0xFNNN.'''
        self.table_0xFNNN[self.opcode[2:4]]()

    def inst_0x00E0(self):
        '''0x00E0: Clears the screen.'''
        self.gfx = [[0 for x in range(32)] for y in range(64)]
        self.draw_flag = True
        self.pc += 2

    def inst_0x00EE(self):
        '''0x00EE: Returns from subroutine.'''
        self.pc = self.stk.pop()
        self.pc += 2

    def inst_0x1NNN(self):
        '''0x1NNN: Jumps to address NNN.'''
        self.pc = int(self.opcode[1:4], 16)

    def inst_0x2NNN(self):
        '''0x2NNN: Calls subroutine at NNN.'''
        self.stk.push(self.pc)
        self.pc = int(self.opcode[1:4], 16)

    def inst_0x3XNN(self):
        '''0x3XNN: Skips the next instruction if VX equals NN.'''
        if self.V[int(self.opcode[1], 16)] == int(self.opcode[2:4], 16):
            self.pc += 4
        else:
            self.pc += 2

    def inst_0x4XNN(self):
        '''0x4XNN: Skips the next instruction if VX doesn't equal NN.'''
        if self.V[int(self.opcode[1], 16)] != int(self.opcode[2:4], 16):
            self.pc += 4
        else:
            self.pc += 2

    def inst_0x5XY0(self):
        '''0x5XY0: Skips the next instruction if VX equals VY.'''
        if self.V[int(self.opcode[1], 16)] == self.V[int(self.opcode[2] ,16)]:
            self.pc += 4
        else:
            self.pc += 2

    def inst_0x6XNN(self):
        '''0x6XNN: Sets VX to NN.'''
        self.V[int(self.opcode[1], 16)] = int(self.opcode[2:4], 16)
        self.pc += 2

    def inst_0x7XNN(self):
        '''0x7XNN: Adds NN to VX.'''
        self.V[int(self.opcode[1], 16)] += int(self.opcode[2:4], 16)
        self.V[int(self.opcode[1], 16)] &= 255 # Take the lowest 8 bits
        self.pc += 2

    def inst_0x8XY0(self):
        '''0x8XY0: Sets VX to the value of VY.'''
        self.V[int(self.opcode[1], 16)] = self.V[int(self.opcode[2], 16)]
        self.pc += 2

    def inst_0x8XY1(self):
        '''0x8XY1: Sets VX to "VX OR VY".'''
        self.V[int(self.opcode[1], 16)] |= self.V[int(self.opcode[2], 16)]
        self.pc += 2

    def inst_0x8XY2(self):
        '''0x8XY2: Sets VX to "VX AND VY".'''
        self.V[int(self.opcode[1], 16)] &= self.V[int(self.opcode[2], 16)]
        self.pc += 2

    def inst_0x8XY3(self):
        '''0x8XY3: Sets VX to "VX XOR VY".'''
        self.V[int(self.opcode[1], 16)] ^= self.V[int(self.opcode[2], 16)]
        self.pc += 2

    def inst_0x8XY4(self):
        '''0x8XY4: Adds VY to VX. VF is set to 1 when there's a carry, and to
        0 when there isn't.'''
        self.V[int(self.opcode[1], 16)] += self.V[int(self.opcode[2], 16)]
        if sum > 255:
            self.V[15] = 1
            self.V[int(self.opcode[1], 16)] &= 255 # Take the lowest 8 bits
        else:
            self.V[15] = 0
        self.pc += 2

    def inst_0x8XY5(self):
        '''0x8XY5: VY is subtracted from VX. VF is set to 0 when there's a
        borrow, and 1 when there isn't.'''
        if self.V[int(self.opcode[1], 16)] > self.V[int(self.opcode[2], 16)]:
            self.V[0xF] = 1
        else:
            self.V[0xF] = 0 # there is a borrow
        self.V[int(self.opcode[1], 16)] -= self.V[int(self.opcode[2], 16)]
        self.pc += 2

    def inst_0x8XY6(self):
        '''0x8XY6: Shifts VX right by 1. VF is set to the value of the least
        significant bit of VX before the shift.'''
        # Make binary string from integer
        bin_str = bin(self.V[int(self.opcode[1], 16)])
        # Check for least significant bit
        if bin_str[len(bin_str)-1] == "1":
            self.V[15] = 1
        elif bin_str[len(bin_str)-1] == "0":
            self.V[15] = 0
        # Divide Vx by 2 by shifting right by 1
        self.V[int(self.opcode[1], 16)] >>= 1
        self.pc += 2

    def inst_0x8XY7(self):
        '''0x8XY7: Sets VX to VY minus VX. VF is set to 0 when there's a
        borrow, and 1 when there isn't.'''
        if self.V[int(self.opcode[2], 16)] > self.V[int(self.opcode[1], 16)]:
            self.V[0xF] = 1
        else:
            self.V[0xF] = 0
        self.V[int(self.opcode[1], 16)] = self.V[int(self.opcode[2], 16)] - \
            self.V[int(self.opcode[1], 16)]
        self.pc += 2

    def inst_0x8XYE(self):
        '''0x8XYE: Shifts VX left by one. VF is set to the value of the most
        significant bit of VX before the shift.'''
        # Check for least significant bit
        if self.V[int(self.opcode[1], 16)] / 255 > 1:
            self.V[15] = 1
        else:
            self.V[15] = 0
        self.V[int(self.opcode[1], 16)] = \
            (self.V[int(self.opcode[1], 16)] << 1) & 255
        self.pc += 2

    def inst_0x9XY0(self):
        '''0x9XY0: Skips the next instruction if VX doesn't equal VY.'''
        if self.V[int(self.opcode[1], 16)] != self.V[int(self.opcode[2], 16)]:
            self.pc += 4
        else:
            self.pc += 2

    def inst_0xANNN(self):
        '''ANNN: Sets I to the address NNN.'''
        self.I = int(self.opcode[1:4], 16)
        self.pc += 2

    def inst_0xBNNN(self):
        '''BNNN: Jumps to the address NNN plus V0.'''
        self.pc = int(self.opcode[1:4], 16) + self.V[0]

    def inst_0xCXNN(self):
        '''CXNN: Sets VX to a random number and NN.'''
        seed()
        self.V[int(self.opcode[1], 16)] = \
            (randint(0, 255) & int(self.opcode[2:4], 16))
        self.pc += 2

    def inst_0xDXYN(self):
        '''DXYN: Draws a sprite at coordinate (VX, VY) that has a width of 8
        pixels and a height of N pixels.
        Each row of 8 pixels is read as bit-coded starting from memory location
        I value doesn't change after the execution of this instruction.
        VF is set to 1 if any screen pixels are flipped from set to unset when
        the sprite is drawn,
        and to 0 if that doesn't happen.'''
        x = self.V[int(self.opcode[1], 16)]
        y = self.V[int(self.opcode[2], 16)]
        length = int(self.opcode[3], 16)
        self.V[15] = 0
        data = [] # Hold data to be written to screen
        # Adjust data
        for i in range(length):
            data.append(bin(int(self.ram[self.I + i], 16)))
            data[i] = data[i].replace('0', '', 1)
            data[i] = data[i].replace('b', '', 1)
            # Pad the data so it's 8 chars long
            while len(data[i]) < 8:
                data[i] = '0' + data[i]
        # Drawing system
        for i in range(len(data)):
            spr_row = data[i]
            for j in range(8):
                new_x = x + j
            if new_x >= 64:
                # Wrap to other side
                while new_x >= 64:
                    new_x -= 64
            new_y = y
            if new_y >= 32:
                # Wrap to other side
                while new_y >= 32:
                    new_y -= 32
            # XOR drawing mode
            if spr_row[j] == "1" and self.gfx[new_x][new_y] == 1:
                self.gfx[new_x][new_y] = 0
                self.V[15] = 1
            elif spr_row[j] == "1" and self.gfx[new_x][new_y] == 0:
                self.gfx[new_x][new_y] = 1
            # Move down for next row
            y += 1
        self.draw_flag = True
        self.pc += 2

    def inst_0xEX9E(self):
        '''EX9E: Skips the next instruction if the key stored in VX is
        pressed.'''
        if self.key[self.V[int(self.opcode[1], 16)]] == 1:
            self.pc += 4
        else:
            self.pc += 2

    def inst_0xEXA1(self):
        '''EXA1 Skips the next instruction if the key stored in VX isn't
        pressed.'''
        if self.key[self.V[int(self.opcode[1], 16)]] == 0:
            self.pc += 4
        else:
            self.pc += 2

    def inst_0xFX07(self):
        '''FX07: Sets VX to the value of the delay timer.'''
        self.V[int(self.opcode[1], 16)] = self.timers[0]
        self.pc += 2

    def inst_0xFX0A(self):
        '''FX0A: A key press is awaited, and then stored in VX.'''
        key_press = False
        for i in range(16):
            if self.key[i] == 1:
                self.V[int(self.opcode[1], 16)] = i
            key_press = True
        # If we didn't received a keypress, skip this cycle and try again.
        if not key_press:
            return
        self.pc += 2

    def inst_0xFX15(self):
        '''FX15: Sets the delay timer to VX.'''
        self.timers[0] = self.V[int(self.opcode[1], 16)]
        self.pc += 2

    def inst_0xFX18(self):
        '''FX18: Sets the sound timer to VX.'''
        self.timers[1] = self.V[int(self.opcode[1], 16)]
        self.pc += 2

    def inst_0xFX1E(self):
        '''FX1E: Adds VX to I.'''
        self.I += self.V[int(self.opcode[1], 16)]
        self.pc += 2

    def inst_0xFX29(self):
        '''FX29: Sets I to the location of the sprite for the character in
        VX.'''
        # Characters 0-F (in hexadecimal) are represented by a 4x5 font
        self.I = (self.V[int(self.opcode[1], 16)] * 5)
        self.pc += 2

    def inst_0xFX33(self):
        '''FX33: Stores the Binary-coded decimal representation of VX at the
        addresses I, I plus 1, and I plus 2.'''
        num = self.V[int(self.opcode[1], 16)]
        self.ram[self.I] = hex(num / 100).replace('x', "")
        num -= 100 * (num / 100)
        self.ram[self.I + 1] = hex(num / 10).replace('x', "")
        num -= 10 * (num / 10)
        self.ram[self.I + 2] = hex(num).replace('x', "")
        self.pc += 2

    def inst_0xFX55(self):
        '''FX55: Stores V0 to VX in memory starting at address I.'''
        for i in range(int(self.opcode[1], 16) + 1):
            self.ram[self.I + i] = hex(self.V[i]).replace('x', "")
        self.pc += 2

    def inst_0xFX65(self):
        '''FX65: Fills V0 to VX with values from memory starting at address
        I.'''
        for i in range(int(self.opcode[1], 16) + 1):
            self.V[i] = int(self.ram[self.I + i], 16)
        self.pc += 2
