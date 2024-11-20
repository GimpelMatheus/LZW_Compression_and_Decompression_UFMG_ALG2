class LZWDecoder:
    """Classe para descompressão de dados codificados com o algoritmo LZW usando expansão dinâmica do dicionário."""

    def __init__(self, max_bits=12):
        self.max_bits = max_bits
        self.dictionary = {}

    def _initialize_dictionary(self):
        """Inicializa o dicionário com as entradas ASCII."""
        self.dictionary = {i: chr(i) for i in range(256)}
        self.next_code = 256

    def decompress(self, codes):
        """Descompressão dos dados a partir de uma lista de códigos."""
        if not codes:
            return ""

        self._initialize_dictionary()
        max_table_size = 1 << self.max_bits

        # Verifica se o primeiro código está no dicionário, caso contrário, inicializa-o
        output = []
        prev_code = codes[0]
        if prev_code not in self.dictionary:
            self.dictionary[prev_code] = chr(prev_code % 256)  # Adiciona uma entrada padrão
        output.append(self.dictionary[prev_code])

        for code in codes[1:]:
            if code in self.dictionary:
                entry = self.dictionary[code]
            else:
                # Tratamento para casos em que o código ainda não está no dicionário
                entry = self.dictionary[prev_code] + self.dictionary[prev_code][0]

            output.append(entry)

            # Adiciona uma nova sequência ao dicionário, se houver espaço
            if self.next_code < max_table_size:
                new_entry = self.dictionary[prev_code] + entry[0]
                self.dictionary[self.next_code] = new_entry
                self.next_code += 1

            prev_code = code

        return "".join(output)
