# utils.py

def read_file(filepath):
    """Lê o conteúdo do arquivo e retorna como string."""
    with open(filepath, "r") as file:
        return file.read()

def write_file(filepath, data):
    """Escreve o conteúdo fornecido no arquivo."""
    with open(filepath, "w") as file:
        file.write(data)
