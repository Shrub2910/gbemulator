import io


def load_rom_byte_stream(rom_path):
    with open(rom_path, "rb") as file:
        byte_stream = file.read()
        return io.BytesIO(byte_stream)
