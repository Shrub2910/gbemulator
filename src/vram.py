from memory import Memory

class VRam(Memory):
    L_BOUNDARY = 0x8000
    U_BOUNDARY = 0x9FFF

    def __init__(self):
        self.data = [0] * 0x4000
    
    def get_value_at_address(self,address):
        return self.data[address-L_boundary]

    def set_value_at_address(self,address,value):
        self.data[address-L_boundary] = value
