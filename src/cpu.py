class Cpu:
    ROM_BOUNDARY = 0x8000
    VRAM_BOUNDARY = 0xA000
    EXTERNAL_BOUNDARY = 0xC000
    RAM_BOUNDARY = 0xE000
    ECHO_BOUNDARY = 0xFE00
    OAM_BOUNDARY = 0xFEA0
    UNUSED_BOUNDARY = 0xFF00
    IO_REGISTER_BOUNDARY = 0xFF80
    HIGH_RAM_BOUNDARY = 0xFFFF
    INTERRUPT_REGISTER_LOCATION = 0xFFFF

    ZERO_FLAG = 7
    SUBTRACTION_FLAG = 6
    HALF_CARRY_FLAG = 5
    CARRY_FLAG = 4

    def __init__(self, rom, ram, vram):
        self.pc = 0x0000
        self.sp = 0xFFFE
        self.A = 0x00
        self.B = 0x00
        self.C = 0x00
        self.D = 0x00
        self.E = 0x00
        self.F = 0x00
        self.H = 0x00
        self.L = 0x00
        self.t_cycles = 0
        self.rom = rom
        self.ram = ram
        self.vram = vram

    def get_register_AF(self):
        return self.F + (self.A << 8)

    def set_register_AF(self, value):
        self.F = value & 0xFF
        self.A = value >> 8

    def get_register_BC(self):
        return self.C + (self.B << 8)

    def set_register_BC(self, value):
        self.C = value & 0xFF
        self.B = value >> 8

    def get_register_DE(self):
        return self.E + (self.D << 8)

    def set_register_DE(self, value):
        self.E = value & 0xFF
        self.D = value >> 8

    def get_register_HL(self):
        return self.L + (self.H << 8)

    def set_register_HL(self, value):
        self.L = value & 0xFF
        self.H = value >> 8

    def get_next_byte(self):
        byte = self.read_address(self.pc)
        self.pc += 1
        return byte

    def set_flag(self, flag, value):
        if value:
            self.F |= (1 << flag)
        else:
            self.F &= ~(1 << flag)

    def increment_flags(self, a):
        b = 1
        result = a + b
        self.set_flag(Cpu.ZERO_FLAG, (result & 0xFF) == 0)
        self.set_flag(Cpu.SUBTRACTION_FLAG, False)
        self.set_flag(Cpu.HALF_CARRY_FLAG, ((a & 0xF) + (b & 0xF)) > 0xF)

    def decrement_flags(self, a):
        b = 1
        result = a - b
        self.set_flag(Cpu.ZERO_FLAG, (result & 0xFF) == 0)
        self.set_flag(Cpu.SUBTRACTION_FLAG, True)
        self.set_flag(Cpu.HALF_CARRY_FLAG, ((a & 0xF) - (b & 0xF)) < 0)

    def add_HL_flags(self, a, b):
        result = a + b
        self.set_flag(Cpu.SUBTRACTION_FLAG, False)
        self.set_flag(Cpu.HALF_CARRY_FLAG, ((a & 0xFFF) + (b & 0xFFF)) > 0xFFF)
        self.set_flag(Cpu.CARRY_FLAG, result > 0xFFFF)

    def zero_flags(self):
        self.F = 0

    def read_address(self, address):
        if address < Cpu.ROM_BOUNDARY:
            return self.rom.get_value_at_address(address)
        elif address < Cpu.VRAM_BOUNDARY:
            return self.vram.get_value_at_address(address)
        elif address < Cpu.EXTERNAL_BOUNDARY:
            raise NotImplementedError("External not implemented")
        elif address < Cpu.RAM_BOUNDARY:
            return self.ram.get_value_at_address(address)
        elif address < Cpu.ECHO_BOUNDARY:
            raise NotImplementedError("Echo not implemented")
        elif address < Cpu.OAM_BOUNDARY:
            raise NotImplementedError("OAM not implemented")
        elif address < Cpu.UNUSED_BOUNDARY:
            raise NotImplementedError("Unused not implemented")
        elif address < Cpu.IO_REGISTER_BOUNDARY:
            raise NotImplementedError("IO register not implemented")
        elif address < Cpu.HIGH_RAM_BOUNDARY:
            raise NotImplementedError("High ram not implemented")
        elif address == Cpu.INTERRUPT_REGISTER_LOCATION:
            raise NotImplementedError("Interrupt register not implemented")
        self.m_cycle()

    def write_address(self, address, value):
        if address < Cpu.ROM_BOUNDARY:
            raise Exception("Cannot write to rom address")
        elif address < Cpu.VRAM_BOUNDARY:
            self.vram.set_value_at_address(address, value)
        elif address < Cpu.EXTERNAL_BOUNDARY:
            raise NotImplementedError("External not implemented")
        elif address < Cpu.RAM_BOUNDARY:
            self.ram.set_value_at_address(address, value)
        elif address < Cpu.ECHO_BOUNDARY:
            raise NotImplementedError("Echo not implemented")
        elif address < Cpu.OAM_BOUNDARY:
            raise NotImplementedError("OAM not implemented")
        elif address < Cpu.UNUSED_BOUNDARY:
            raise NotImplementedError("Unused not implemented")
        elif address < Cpu.IO_REGISTER_BOUNDARY:
            raise NotImplementedError("IO register not implemented")
        elif address < Cpu.HIGH_RAM_BOUNDARY:
            raise NotImplementedError("High ram not implemented")
        elif address == Cpu.INTERRUPT_REGISTER_LOCATION:
            raise NotImplementedError("Interrupt register not implemented")
        self.m_cycle()

    def read_immediate_8(self):
        value = self.read_address(self.pc)
        self.pc += 1

        return value

    def read_immediate_16(self):
        lower = self.read_address(self.pc)
        self.pc += 1
        upper = self.read_address(self.pc)
        self.pc += 1
        upper = upper << 8

        return upper + lower

    def set_a16(self, value):
        address = self.read_immediate_16()
        self.write_address(address, value)

    def m_cycle(self):
        for i in range(0, 4):
            self.t_cycles += 1

    def run(self):
        while True:
            opcode = self.get_next_byte()
            match opcode:
                case 0x00:
                    pass
                case 0x01:
                    self.set_register_BC(self.read_immediate_16())
                case 0x02:
                    self.write_address(self.get_register_BC(), self.A)
                case 0x03:
                    value = self.get_register_BC()
                    value += 1
                    value &= 0xFFFF
                    self.m_cycle()
                    self.set_register_BC(value)
                case 0x04:
                    self.decrement_flags(self.B)
                    self.B += 1
                    self.B &= 0xFF
                case 0x05:
                    self.decrement_flags(self.B)
                    self.B -= 1
                    self.B &= 0xFF
                case 0x06:
                    self.B = self.read_immediate_8()
                case 0x07:
                    self.zero_flags()
                    self.set_flag(Cpu.CARRY_FLAG, (self.A << 1) > 0xFF)
                    bit7 = (self.A >> 7) & 1

                    self.A = ((self.A << 1) | bit7) & 0xFF
                case 0x08:
                    self.set_a16(self.sp)
                case 0x09:
                    value1 = self.get_register_HL()
                    value2 = self.get_register_BC()

                    self.add_HL_flags(value1, value2)

                    result = value1 + value2
                    result &= 0xFFFF
                    self.m_cycle()

                    self.set_register_HL(result)
                case 0x0A:
                    self.A = self.read_address(self.get_register_BC())
                case 0x0B:
                    value = self.get_register_BC()
                    value -= 1
                    value &= 0xFFFF
                    self.m_cycle()
                    self.set_register_BC(value)
                case 0x0C:
                    self.increment_flags(self.C)
                    self.C += 1
                    self.C &= 0xFF
                case 0x0D:
                    self.decrement_flags(self.C)
                    self.C -= 1
                    self.C &= 0xFF
                case 0x0E:
                    self.C = self.read_immediate_8()
                case 0x0F:
                    self.zero_flags()
                    bit0 = self.A & 1
                    self.set_flag(Cpu.CARRY_FLAG, bit0)

                    self.A = ((self.A >> 1) | bit0 << 7) & 0xFF
