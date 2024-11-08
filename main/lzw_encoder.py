from trie import Trie

class LZWEncoder:
    """Classe para compressão de dados usando o algoritmo LZW."""

    def __init__(self, max_bits=12):
        self.max_bits = max_bits
        self.max_table_size = 1 << max_bits  # Tamanho máximo do dicionário
        self.trie = Trie()
        self._initialize_dictionary()

    def _initialize_dictionary(self):
        """Inicializa o dicionário com a tabela ASCII padrão."""
        for i in range(256):
            self.trie.insert(chr(i), i)
        self.next_code = 256

    def compress(self, data):
        """Compressão de dados usando LZW. Retorna uma lista de códigos."""
        current_string = ""
        codes = []
        for char in data:
            combined_string = current_string + char
            if self.trie.search(combined_string) is not None:
                current_string = combined_string
            else:
                codes.append(self.trie.search(current_string))
                if self.next_code < self.max_table_size:
                    self.trie.insert(combined_string, self.next_code)
                    self.next_code += 1
                current_string = char

        if current_string:
            codes.append(self.trie.search(current_string))

        return codes
