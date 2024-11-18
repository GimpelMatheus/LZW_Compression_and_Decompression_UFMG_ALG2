# utils.py
from struct import pack, unpack

def read_file(filepath):
    """Lê o conteúdo do arquivo e retorna como string."""
    if ".bin" in filepath or ".bmp" in filepath:
        with open(filepath, "rb") as file:
            return file.read()
    else:
        with open(filepath, "r") as file:
            return file.read()
    
def read_compressed_file(filepath):
    """Lê o conteúdo do arquivo compresso e retorna como lista de códigos binários."""
    codes = []
    with open(filepath, "rb") as file:
        while True:
            data = file.read(2)
            if not data:
                break
            (code, ) = unpack('>H', data)

            codes.append(code)
        return codes

def write_file(filepath, data):
    """Escreve o conteúdo fornecido no arquivo."""
    with open(filepath, "w") as file:
        file.write(data)

def write_compressed_file(filepath, data):
    """Escreve o conteúdo comprimido no arquivo."""
    with open(filepath, "wb") as file:
        for code in data:
            if isinstance(code, int):
                file.write(pack('>H', code))
            else:
                file.write(pack('>H', int(ord(code))))
