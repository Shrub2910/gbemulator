from memory import Memory


class Ram(Memory):
    L_BOUNDARY = 0xC000
    U_BOUNDARY = 0xDFFF

    def __init__(self):
        self.data = [0]*0x2000

    def get_value_at_address(self, address):
        return self.data[address - Ram.L_BOUNDARY]

    def set_value_at_address(self, address, value):
        self.data[address - Ram.L_BOUNDARY] = value
