from memory import Memory


class Rom(Memory):
    L_BOUNDARY = 0x0000
    U_BOUNDARY = 0x7FFF
    
    def __init__(self):
        self.data = [0]*0x8000

    def get_value_at_address(self, address):
        return self.data[address]
    
    def set_value_at_address(self, address, value):
        raise Exception("Cannot write to ROM")
