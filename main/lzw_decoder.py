class LZWDecoder:
    """Classe para descompressão de dados codificados com o algoritmo LZW."""

    def __init__(self, max_bits=12):
        self.max_bits = max_bits
        self.max_table_size = 1 << max_bits  # Tamanho máximo do dicionário
        self.dictionary = {}
        self._initialize_dictionary()

    def _initialize_dictionary(self):
        """Inicializa o dicionário com a tabela ASCII padrão."""
        for i in range(256):
            self.dictionary[i] = chr(i)
        self.next_code = 256

    def decompress(self, codes):
        """Descompressão dos dados a partir de uma lista de códigos."""
        output = []
        prev_code = codes[0]
        output.append(self.dictionary[prev_code])

        for code in codes[1:]:
            if code not in self.dictionary:
                entry = self.dictionary[prev_code] + self.dictionary[prev_code][0]
            else:
                entry = self.dictionary[code]

            output.append(entry)

            if self.next_code < self.max_table_size:
                self.dictionary[self.next_code] = self.dictionary[prev_code] + entry[0]
                self.next_code += 1

            prev_code = code

        return "".join(output)
