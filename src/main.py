import rom_loader

def main():
    rom_path = input()
    rom_loader.load_rom_byte_stream(rom_path)

if __name__ == "__main__":
    main()
