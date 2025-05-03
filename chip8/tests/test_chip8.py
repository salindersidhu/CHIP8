import unittest
from chip8.chip8 import Chip8

class TestChip8(unittest.TestCase):
    def setUp(self):
        self.chip8 = Chip8()
        self.chip8.reset()

    def set_opcode(self, opcode_hex):
        # Set opcode in RAM at current PC, always use lowercase for CHIP-8
        opcode_hex = opcode_hex.lower()
        pc = self.chip8.getState()['PRC']
        self.chip8._Chip8__ram[pc] = opcode_hex[:2]
        self.chip8._Chip8__ram[pc+1] = opcode_hex[2:]
        self.chip8._Chip8__opCode = opcode_hex

    def test_reset_initializes_state(self):
        self.chip8.reset()
        state = self.chip8.getState()
        self.assertEqual(state['PRC'], 512)
        self.assertEqual(state['ADR'], 0)
        self.assertEqual(state['OPC'], 0)
        self.assertEqual(state['TIM'], [0, 0])
        self.assertEqual(len(state['GFX']), 64)
        self.assertEqual(len(state['GFX'][0]), 32)
        self.assertEqual(state['KEY'], [0]*16)
        self.assertEqual(state['REG'], [0]*16)
        self.assertEqual(len(state['RAM']), 4096)
        # Fontset loaded
        self.assertNotEqual(state['RAM'][0:80], ['00']*80)

    def test_setKeyState(self):
        self.chip8.reset()
        self.chip8.setKeyState(2, 1)
        state = self.chip8.getState()
        self.assertEqual(state['KEY'][2], 1)
        self.chip8.setKeyState(2, 0)
        state = self.chip8.getState()
        self.assertEqual(state['KEY'][2], 0)

    def test_getSoundTimer(self):
        self.chip8.reset()
        self.assertEqual(self.chip8.getSoundTimer(), 0)
        # Set timer and check
        self.chip8._Chip8__timers[1] = 5
        self.assertEqual(self.chip8.getSoundTimer(), 5)

    def test_getGFX(self):
        self.chip8.reset()
        gfx = self.chip8.getGFX()
        self.assertEqual(len(gfx), 64)
        self.assertEqual(len(gfx[0]), 32)

    def test_get_and_set_state(self):
        self.chip8.reset()
        state = self.chip8.getState()
        # Change state and set it back
        state['PRC'] = 999
        self.chip8.setState(state)
        self.assertEqual(self.chip8.getState()['PRC'], 999)

    def test_loadROM_sets_memory(self):
        self.chip8.reset()
        # Create a fake ROM file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b'\x01\x02\x03\x04')
            tmp.flush()
            self.chip8.loadROM(tmp.name)
        state = self.chip8.getState()
        # ROM should be loaded at 0x200 (512)
        self.assertEqual(state['RAM'][512], '01')
        self.assertEqual(state['RAM'][513], '02')
        self.assertEqual(state['RAM'][514], '03')
        self.assertEqual(state['RAM'][515], '04')

    def test_00E0_clear_screen(self):
        self.set_opcode('00E0')
        self.chip8._Chip8__gfx[0][0] = 1
        self.chip8.emulateCycle()
        self.assertTrue(all(all(px == 0 for px in row) for row in self.chip8.getGFX()))

    def test_00EE_return_subroutine(self):
        self.chip8._Chip8__stk.push(600)
        self.set_opcode('00EE')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8.getState()['PRC'], 602)

    def test_1NNN_jump(self):
        self.set_opcode('1123')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8.getState()['PRC'], 0x123)

    def test_2NNN_call_subroutine(self):
        self.set_opcode('2456')
        old_pc = self.chip8.getState()['PRC']
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8.getState()['PRC'], 0x456)
        self.assertEqual(self.chip8._Chip8__stk.pop(), old_pc)

    def test_3XNN_skip_if_equal(self):
        self.chip8._Chip8__V[1] = 0xAB
        self.set_opcode('31AB')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8.getState()['PRC'], 516)  # +4

    def test_4XNN_skip_if_not_equal(self):
        self.chip8._Chip8__V[2] = 0x10
        self.set_opcode('4211')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8.getState()['PRC'], 516)  # +4, since 0x10 != 0x11

    def test_5XY0_skip_if_vx_eq_vy(self):
        self.chip8._Chip8__V[3] = 0x22
        self.chip8._Chip8__V[4] = 0x22
        self.set_opcode('5340')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8.getState()['PRC'], 516)

    def test_6XNN_set_vx(self):
        self.set_opcode('60FF')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8._Chip8__V[0], 0xFF)

    def test_7XNN_add_vx(self):
        self.chip8._Chip8__V[1] = 1
        self.set_opcode('7101')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8._Chip8__V[1], 2)

    def test_8XY0_set_vx_to_vy(self):
        self.chip8._Chip8__V[2] = 0x55
        self.chip8._Chip8__V[3] = 0x77
        self.set_opcode('8230')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8._Chip8__V[2], 0x77)

    def test_8XY1_or(self):
        self.chip8._Chip8__V[2] = 0xF0
        self.chip8._Chip8__V[3] = 0x0F
        self.set_opcode('8231')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8._Chip8__V[2], 0xFF)

    def test_8XY2_and(self):
        self.chip8._Chip8__V[2] = 0xF0
        self.chip8._Chip8__V[3] = 0x0F
        self.set_opcode('8232')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8._Chip8__V[2], 0x00)

    def test_8XY3_xor(self):
        self.chip8._Chip8__V[2] = 0xF0
        self.chip8._Chip8__V[3] = 0x0F
        self.set_opcode('8233')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8._Chip8__V[2], 0xFF)

    def test_8XY4_add_with_carry(self):
        self.chip8._Chip8__V[2] = 0xFF
        self.chip8._Chip8__V[3] = 0x02
        self.set_opcode('8234')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8._Chip8__V[2], 1)
        self.assertEqual(self.chip8._Chip8__V[15], 1)

    def test_8XY5_subtract(self):
        self.chip8._Chip8__V[2] = 5
        self.chip8._Chip8__V[3] = 2
        self.set_opcode('8235')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8._Chip8__V[2], 3)
        self.assertEqual(self.chip8._Chip8__V[15], 1)

    def test_8XY6_shift_right(self):
        self.chip8._Chip8__V[2] = 0b101
        self.set_opcode('8206')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8._Chip8__V[2], 0b10)
        self.assertEqual(self.chip8._Chip8__V[15], 1)

    def test_8XY7_set_vx_to_vy_minus_vx(self):
        self.chip8._Chip8__V[2] = 2
        self.chip8._Chip8__V[3] = 5
        self.set_opcode('8237')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8._Chip8__V[2], 3)
        self.assertEqual(self.chip8._Chip8__V[15], 1)

    def test_8XYE_shift_left(self):
        self.chip8._Chip8__V[2] = 0b10000001
        self.set_opcode('820E')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8._Chip8__V[2], 2)
        self.assertEqual(self.chip8._Chip8__V[15], 1)

    def test_9XY0_skip_if_vx_not_eq_vy(self):
        self.chip8._Chip8__V[2] = 1
        self.chip8._Chip8__V[3] = 2
        self.set_opcode('9230')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8.getState()['PRC'], 516)

    def test_ANNN_set_I(self):
        self.set_opcode('A123')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8.getState()['ADR'], 0x123)

    def test_BNNN_jump_v0(self):
        self.chip8._Chip8__V[0] = 5
        self.set_opcode('B200')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8.getState()['PRC'], 0x200 + 5)

    def test_CXNN_random(self):
        self.set_opcode('C0FF')
        self.chip8.emulateCycle()
        self.assertTrue(0 <= self.chip8._Chip8__V[0] <= 0xFF)

    def test_EX9E_skip_if_key_pressed(self):
        self.chip8._Chip8__V[1] = 2
        self.chip8._Chip8__key[2] = 1
        self.set_opcode('E19E')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8.getState()['PRC'], 516)

    def test_EXA1_skip_if_key_not_pressed(self):
        self.chip8._Chip8__V[1] = 2
        self.chip8._Chip8__key[2] = 0
        self.set_opcode('E1A1')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8.getState()['PRC'], 516)

    def test_FX07_set_vx_to_delay_timer(self):
        self.chip8._Chip8__timers[0] = 7
        self.set_opcode('F107')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8._Chip8__V[1], 7)

    def test_FX15_set_delay_timer(self):
        self.chip8._Chip8__V[1] = 9
        self.set_opcode('F115')
        self.chip8.emulateCycle()
        # Timer is set to 9, then decremented to 8 in the same cycle
        self.assertEqual(self.chip8._Chip8__timers[0], 8)

    def test_FX18_set_sound_timer(self):
        self.chip8._Chip8__V[1] = 8
        self.set_opcode('F118')
        self.chip8.emulateCycle()
        # Timer is set to 8, then decremented to 7 in the same cycle
        self.assertEqual(self.chip8._Chip8__timers[1], 7)

    def test_FX1E_add_vx_to_I(self):
        self.chip8._Chip8__V[1] = 5
        self.set_opcode('F11E')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8.getState()['ADR'], 5)

    def test_FX29_set_I_to_sprite(self):
        self.chip8._Chip8__V[1] = 2
        self.set_opcode('F129')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8.getState()['ADR'], 10)

    def test_FX33_bcd(self):
        self.chip8._Chip8__V[1] = 123
        self.chip8._Chip8__I = 100
        self.set_opcode('F133')
        self.chip8.emulateCycle()
        ram = self.chip8._Chip8__ram
        self.assertEqual(ram[100], '01')
        self.assertEqual(ram[101], '02')
        self.assertEqual(ram[102], '03')

    def test_FX55_store_registers(self):
        self.chip8._Chip8__V[0] = 1
        self.chip8._Chip8__V[1] = 2
        self.chip8._Chip8__I = 200
        self.set_opcode('F155')
        self.chip8.emulateCycle()
        ram = self.chip8._Chip8__ram
        self.assertEqual(ram[200], '01')
        self.assertEqual(ram[201], '02')

    def test_FX65_load_registers(self):
        self.chip8._Chip8__ram[200] = '01'
        self.chip8._Chip8__ram[201] = '02'
        self.chip8._Chip8__I = 200
        self.set_opcode('F165')
        self.chip8.emulateCycle()
        self.assertEqual(self.chip8._Chip8__V[0], 1)
        self.assertEqual(self.chip8._Chip8__V[1], 2)
