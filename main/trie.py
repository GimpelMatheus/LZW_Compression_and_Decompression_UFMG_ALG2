class TrieNode:
    """Representa um nó na Trie."""
    def __init__(self):
        self.children = {}
        self.code = None

class Trie:
    """Implementa a estrutura Trie para gerenciar o dicionário LZW."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, string, code):
        """Insere uma string na Trie associada a um código."""
        node = self.root
        for char in string:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.code = code

    def search(self, string):
        """Busca uma string na Trie. Retorna o código ou None se não encontrado."""
        node = self.root
        for char in string:
            if char not in node.children:
                return None
            node = node.children[char]
        return node.code

    def starts_with(self, prefix):
        """Verifica se existe uma string na Trie que começa com o prefixo dado."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
