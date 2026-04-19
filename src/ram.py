class Ram:
    
    def __init__(self):
        self.memory = [0] * 8000

    def get_value_at_address(self, address):
        return self.memory[address]

    def set_value_at_address(self, address, value):
        self.memory[address] = value

##ram = Ram()
##ram.set_value_at_address(40,7)
##print(ram.get_value_at_address(40))
