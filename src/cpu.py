class Cpu:
    def __init__(self, program_data):
        self.program_data = program_data
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
        self.m_cycles = 0

    def get_next_byte(self):
        byte = self.program_data[self.pc]
        self.pc += 1
        return byte

    def run(self):
        while True:
            opcode = self.get_next_byte()
            self.m_cycles += self.step(opcode)

    def step(self, opcode):
        match opcode:
            case 0x00:
                return 1
