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
                match_len = len(child_value)
                if string[i:].startswith(child_value):
                    node = child_node
                    i += match_len
                    found = True
                    break
                elif string[i:i + match_len] == child_value[:match_len]:
                    split_node = TrieNode()
                    split_node.value = child_value[:match_len]
                    split_node.children[child_value[match_len:]] = child_node
                    node.children[string[i:i + match_len]] = split_node
                    node = split_node
                    i += match_len
                    found = True
                    break
            if not found:
                new_node = TrieNode()
                new_node.value = string[i:]
                node.children[string[i:]] = new_node
                node = new_node
                i = len(string)
        node.code = code

    def search(self, string):
        """Busca uma string na Trie compacta. Retorna o código ou None se não encontrado."""
        node = self.root
        i = 0
        while i < len(string):
            found = False
            for child_value, child_node in node.children.items():
                if string[i:].startswith(child_value):
                    node = child_node
                    i += len(child_value)
                    found = True
                    break
            if not found:
                return None
        return node.code
    def delete(self, string):
        """Remove uma string da Trie compacta se ela existir."""

        def _delete(node, string, depth, parent=None, parent_key=None):
            # Caso base: fim da string
            if depth == len(string):
                if node.code is not None:
                    node.code = None  # Remove o código
                    # Se o nó não tem filhos, ele pode ser removido
                    return len(node.children) == 0
                return False  # A string não estava armazenada como código

            # Percorre os filhos para encontrar o próximo segmento
            for child_value, child_node in list(node.children.items()):
                if string[depth:].startswith(child_value):
                    # Chamada recursiva no nó filho
                    should_delete_child = _delete(child_node, string, depth + len(child_value), node, child_value)

                    # Se o filho deve ser removido, faz a exclusão
                    if should_delete_child:
                        del node.children[child_value]

                        # Verifica se o nó atual se tornou um nó intermediário desnecessário
                        if parent and len(node.children) == 1 and node.code is None:
                            # Obtenha o único filho remanescente e combine com o pai
                            only_child_key, only_child_node = next(iter(node.children.items()))
                            combined_key = child_value + only_child_key

                            # Reatribui o filho combinado ao nó avô
                            parent.children[parent_key] = only_child_node
                            only_child_node.value = combined_key  # Atualiza o valor combinado

                        # Retorna True para indicar que o nó atual também pode ser excluído
                        return len(node.children) == 0 and node.code is None
                    return True

            return False  # Se a string não corresponde a um caminho válido

        # Inicia a remoção a partir da raiz
        return _delete(self.root, string, 0)


    def starts_with(self, prefix):
        """Verifica se existe uma string na Trie que começa com o prefixo dado."""
        node = self.root
        i = 0
        while i < len(prefix):
            found = False
            for child_value, child_node in node.children.items():
                # Modificação para aceitar prefixos incompletos
                if prefix[i:].startswith(child_value):
                    node = child_node
                    i += len(child_value)
                    found = True
                    break
                elif child_value.startswith(prefix[i:]):
                    return True  # Prefixo é uma subsequência de um nó existente
            if not found:
                return False
        return True

    def show(self):
        """Mostra todos os valores da Trie com seus códigos usando pré-ordem."""
        def _show(node, prefix):
            if node.code is not None:
                print(f"{prefix}: {node.code}")
            for child_value, child_node in node.children.items():
                _show(child_node, prefix + child_value)

        _show(self.root, "")
