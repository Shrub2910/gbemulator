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
    INTERUPT_REGISTER_LOCATION = 0xFFFF

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
        self.m_cycle()
        return self.a + (self.f << 8)

    def set_register_AF(self, value):
        self.A = value & 0xFF
        self.F = value >> 8
        self.m_cycle()

    def get_register_BC(self):
        self.m_cycle()
        return self.B + (self.C << 8)

    def set_register_BC(self, value):
        self.B = value & 0xFF
        self.C = value >> 8
        self.m_cycle()

    def get_register_DE(self):
        self.m_cycle()
        return self.D + (self.E << 8)

    def set_register_DE(self, value):
        self.D = value & 0xFF
        self.E = value >> 8
        self.m_cycle()

    def get_register_HL(self):
        self.m_cycle()
        return self.H + (self.L << 8)

    def set_register_HL(self, value):
        self.H = value & 0xFF
        self.L = value >> 8
        self.m_cycle()

    def get_next_byte(self):
        byte = self.read_address(self.pc)
        self.pc += 1
        return byte

    def read_address(self, address):
        if address < Cpu.ROM_BOUNDARY:
            return self.rom.get_value_at_address(address)
        elif address < Cpu.VRAM_BOUNDARY:
            return self.vram.get_value_at_address(address)
        elif address < Cpu.EXTERNAL_BOUNDARY:
            pass
        elif address < Cpu.RAM_BOUNDARY:
            return self.ram.get_value_at_address(address)
        elif address < Cpu.ECHO_BOUNDARY:
            pass
        elif address < Cpu.OAM_BOUNDARY:
            pass
        elif address < Cpu.UNUSED_BOUNDARY:
            pass
        elif address < Cpu.IO_REGISTER_BOUNDARY:
            pass
        elif address < Cpu.HIGH_RAM_BOUNDARY:
            pass
        elif address == Cpu.INTERUPT_REGISTER_LOCATION:
            pass
        self.m_cycle()

    def write_address(self, address, value):
        if address < Cpu.ROM_BOUNDARY:
            raise Exception("Cannot write to rom address")
        elif address < Cpu.VRAM_BOUNDARY:
            self.vram.set_value_at_address(address, value)
        elif address < Cpu.EXTERNAL_BOUNDARY:
            pass
        elif address < Cpu.RAM_BOUNDARY:
            self.ram.set_value_at_address(address, value)
        elif address < Cpu.ECHO_BOUNDARY:
            pass
        elif address < Cpu.OAM_BOUNDARY:
            pass
        elif address < Cpu.UNUSED_BOUNDARY:
            pass
        elif address < Cpu.IO_REGISTER_BOUNDARY:
            pass
        elif address < Cpu.HIGH_RAM_BOUNDARY:
            pass
        elif address == Cpu.INTERUPT_REGISTER_LOCATION:
            pass
        self.m_cycle()

    def read_immediate_16(self):
        lower = self.rom.get_value_at_address(self.pc)
        self.pc += 1
        upper = self.rom.get_value_at_address(self.pc)
        self.pc += 1

        upper = upper << 8

        self.m_cycle()

        return upper + lower

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
