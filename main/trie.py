class TrieNode:
    """Representa um nó em uma Trie compacta para LZW."""
    def __init__(self):
        self.children = {}
        self.code = None
        self.value = ""  # Armazena a sequência de caracteres compactados

class Trie:
    """Implementa uma Trie compacta para gerenciar o dicionário LZW."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, string, code):
        """Insere uma string compactada na Trie associada a um código."""
        node = self.root
        i = 0
        while i < len(string):
            found = False
            for child_value, child_node in node.children.items():
                # Se o prefixo do nó filho atual corresponde ao restante da string
                if string[i:].startswith(child_value):
                    node = child_node
                    i += len(child_value)
                    found = True
                    break
            if not found:
                # Adiciona um novo nó com a parte restante da string
                new_node = TrieNode()
                new_node.value = string[i:]
                node.children[string[i:]] = new_node
                node = new_node
                i = len(string)  # Finaliza o loop
        node.code = code

    def search(self, string):
        """Busca uma string na Trie compacta. Retorna o código ou None se não encontrado."""
        node = self.root
        i = 0
        while i < len(string):
            found = False
            for child_value, child_node in node.children.items():
                # Verifica se o prefixo do nó filho corresponde ao restante da string
                if string[i:].startswith(child_value):
                    node = child_node
                    i += len(child_value)
                    found = True
                    break
            if not found:
                return None
        return node.code

    def starts_with(self, prefix):
        """Verifica se existe uma string na Trie que começa com o prefixo dado."""
        node = self.root
        i = 0
        while i < len(prefix):
            found = False
            for child_value, child_node in node.children.items():
                if prefix[i:].startswith(child_value):
                    node = child_node
                    i += len(child_value)
                    found = True
                    break
            if not found:
                return False
        return True
