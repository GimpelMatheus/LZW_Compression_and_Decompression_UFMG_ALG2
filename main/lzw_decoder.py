from trie import Trie

class LZWDecoder:
    """Classe para descompressão de dados codificados com o algoritmo LZW usando Trie compacta."""

    def __init__(self, max_bits=12):
        self.max_bits = max_bits
        self.max_table_size = 1 << max_bits  # Tamanho máximo do dicionário
        self.trie = Trie()
        self._initialize_dictionary()

    def _initialize_dictionary(self):
        """Inicializa o dicionário com a tabela ASCII padrão."""
        self.dictionary = {i: chr(i) for i in range(256)}
        for i in range(256):
            self.trie.insert(chr(i), i)
        self.next_code = 256

    def decompress(self, codes):
        """Descompressão dos dados a partir de uma lista de códigos."""
        output = []
        prev_code = codes[0]
        output.append(self.dictionary[prev_code])

        for code in codes[1:]:
            if code not in self.dictionary:
                # Caso especial: o código atual não está no dicionário
                entry = self.dictionary[prev_code] + self.dictionary[prev_code][0]
            else:
                entry = self.dictionary[code]

            # Adiciona a sequência decodificada ao output
            output.append(entry)

            # Adiciona uma nova sequência ao dicionário se houver espaço
            if self.next_code < self.max_table_size:
                new_entry = self.dictionary[prev_code] + entry[0]
                self.dictionary[self.next_code] = new_entry
                self.trie.insert(new_entry, self.next_code)
                self.next_code += 1

            # Atualiza o código anterior
            prev_code = code

        return "".join(output)
