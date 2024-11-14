from trie import Trie

class LZWEncoder:
    """Classe para compressão de dados usando o algoritmo LZW com Trie compacta e formato binário variável."""

    def __init__(self, max_bits=12):
        self.max_bits = max_bits
        self.initial_max_bits = max_bits
        self.trie = Trie()

    def _initialize_dictionary(self):
        """Inicializa o dicionário com as palavras ASCII em formato binário."""
        self.trie = Trie()
        for i in range(256):
            binary_value = format(i, '08b')
            self.trie.insert(binary_value, i)
        self.next_code = 256  # Primeiro código livre após os caracteres ASCII

    def compress(self, data):
        """Compressão de dados com ajuste dinâmico de max_bits para garantir a eficiência."""
        words = data.split()
        original_size = len(data)

        # Converte cada palavra para uma sequência binária
        binary_words = [''.join(format(ord(char), '08b') for char in word) for word in words]
        compressed_data = self._compress_with_max_bits(binary_words)
        compressed_size = len(compressed_data) * (self.max_bits // 8)

        # Ajusta max_bits apenas se necessário
        while compressed_size >= original_size and self.max_bits > 8:
            self.max_bits -= 1
            compressed_data = self._compress_with_max_bits(binary_words)
            compressed_size = len(compressed_data) * (self.max_bits // 8)

        # Se a compressão não reduz o tamanho, retorna o original
        if compressed_size >= original_size:
            print("Compressão aumentou o tamanho do arquivo. Retornando o original.")
            return data

        return compressed_data

    def _compress_with_max_bits(self, binary_words):
        """Compressão de palavras binárias com base em max_bits atual."""
        self._initialize_dictionary()
        max_table_size = 1 << self.max_bits
        current_string = ""
        codes = []

        for binary_word in binary_words:
            combined_string = current_string + binary_word
            if self.trie.search(combined_string) is not None:
                current_string = combined_string
            else:
                if current_string:
                    code = self.trie.search(current_string)
                    if code is not None:
                        codes.append(code)

                if self.next_code < max_table_size:
                    self.trie.insert(combined_string, self.next_code)
                    self.next_code += 1

                current_string = binary_word

        if current_string:
            code = self.trie.search(current_string)
            if code is not None:
                codes.append(code)

        return codes
