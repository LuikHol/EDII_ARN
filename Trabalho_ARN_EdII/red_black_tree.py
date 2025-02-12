from enum import Enum
from collections import deque


class Color(Enum):
    RED = 1
    BLACK = 2

class Node:
    def __init__(self, value, color, parent=None):
        self.value = value # Valor armazenado no nó
        self.color = color # Cor do nó (RED/BLACK)
        self.parent = parent # Nó pai
        self.left = None # Filho esquerdo
        self.right = None # Filho direito
        self.size = 1  # Tamanho da subárvore (para estatísticas de ordem)

class RedBlackTree:
    def __init__(self):
        self.NIL = Node(None, Color.BLACK)
        self.NIL.size = 0 
        self.root = self.NIL

    # ------ Questão 1 ------- 

    def insert(self, value):
        new_node = Node(value, Color.RED)
        new_node.parent = self.NIL
        new_node.left = self.NIL
        new_node.right = self.NIL

        parent = self.NIL
        current = self.root

        # Rastrear o caminho da inserção para atualizar os tamanhos
        path = []
        while current != self.NIL:
            parent = current
            path.append(parent)
            if new_node.value < current.value:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent
        if parent == self.NIL:
            self.root = new_node
        elif new_node.value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node

        # Atualizar os tamanhos dos nós no caminho
        for node in path:
            node.size += 1

        self.insert_fixup(new_node)

    def insert_fixup(self, node):
        while node.parent.color == Color.RED:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == Color.RED:
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self.right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == Color.RED:
                    node.parent.color = Color.BLACK
                    uncle.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = Color.BLACK
                    node.parent.parent.color = Color.RED
                    self.left_rotate(node.parent.parent)
            if node == self.root:
                break
        self.root.color = Color.BLACK

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

        # Atualizar os tamanhos após a rotação
        x.size = x.left.size + x.right.size + 1
        y.size = y.left.size + y.right.size + 1

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

        # Atualizar os tamanhos após a rotação
        x.size = x.left.size + x.right.size + 1
        y.size = y.left.size + y.right.size + 1

    def delete_by_val(self, val):
        node = self.find_node(val)
        if node == self.NIL:
            return
        self.delete_node(node)

    def find_node(self, val):
        current = self.root
        while current != self.NIL:
            if val == current.value:
                return current
            elif val < current.value:
                current = current.left
            else:
                current = current.right
        return self.NIL

    def delete_node(self, node):
        y = node
        y_original_color = y.color
        if node.left == self.NIL:
            x = node.right
            self.transplant(node, node.right)
        elif node.right == self.NIL:
            x = node.left
            self.transplant(node, node.left)
        else:
            y = self.minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            self.transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color
        if y_original_color == Color.BLACK:
            self.delete_fixup(x)

        # Atualizar os tamanhos dos ancestais após a remoção
        self.update_sizes(node.parent)

    def transplant(self, u, v):
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def delete_fixup(self, x):
        while x != self.root and x.color == Color.BLACK:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == Color.RED:
                    s.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.left_rotate(x.parent)
                    s = x.parent.right
                if s.left.color == Color.BLACK and s.right.color == Color.BLACK:
                    s.color = Color.RED
                    x = x.parent
                else:
                    if s.right.color == Color.BLACK:
                        s.left.color = Color.BLACK
                        s.color = Color.RED
                        self.right_rotate(s)
                        s = x.parent.right
                    s.color = x.parent.color
                    x.parent.color = Color.BLACK
                    s.right.color = Color.BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == Color.RED:
                    s.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.right_rotate(x.parent)
                    s = x.parent.left
                if s.right.color == Color.BLACK and s.left.color == Color.BLACK:
                    s.color = Color.RED
                    x = x.parent
                else:
                    if s.left.color == Color.BLACK:
                        s.right.color = Color.BLACK
                        s.color = Color.RED
                        self.left_rotate(s)
                        s = x.parent.left
                    s.color = x.parent.color
                    x.parent.color = Color.BLACK
                    s.left.color = Color.BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = Color.BLACK

    def update_sizes(self, node):
        """Atualiza os tamanhos dos nós no caminho até a raiz"""
        while node != self.NIL:
            node.size = node.left.size + node.right.size + 1
            node = node.parent

    def print_in_order(self):
        self._in_order(self.root)
        print()

    def _in_order(self, node):
        if node != self.NIL:
            self._in_order(node.left)
            print(f"{node.value}({node.color.name})", end=" ")
            self._in_order(node.right)

    # ------ Questão 2 -------  

    def find(self, value):
        """Busca um valor na árvore e retorna True se encontrado, False caso contrário"""
        return self._find(self.root, value)

    def _find(self, node, value):
        if node == self.NIL:
            return False
        if value == node.value:
            return True
        elif value < node.value:
            return self._find(node.left, value)
        else:
            return self._find(node.right, value)

    def find_min(self):
        """Retorna o menor valor da árvore"""
        if self.root == self.NIL:
            return None
        return self._find_min(self.root).value

    def _find_min(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def find_max(self):
        """Retorna o maior valor da árvore"""
        if self.root == self.NIL:
            return None
        return self._find_max(self.root).value

    def _find_max(self, node):
        while node.right != self.NIL:
            node = node.right
        return node
    
    # ------ Questão 3 ------- 

    def find_kth(self, k):
        """Encontra o k-ésimo menor elemento (k >= 1)"""
        if k < 1 or k > self.root.size:
            return None
        return self._find_kth(self.root, k)

    def _find_kth(self, node, k):
        left_size = node.left.size
        if k == left_size + 1:
            return node.value
        elif k <= left_size:
            return self._find_kth(node.left, k)
        else:
            return self._find_kth(node.right, k - (left_size + 1))
        
    # ------ Questão 4 ------- 
        
    def find_interval(self, low, high):
        """Imprime todos os elementos no intervalo [low, high]"""
        self._find_interval(self.root, low, high)
        print()  # Para pular uma linha após a impressão

    def _find_interval(self, node, low, high):
        if node == self.NIL:
            return

        # Se o valor do nó for maior que low, explorar a subárvore esquerda
        if node.value > low:
            self._find_interval(node.left, low, high)

        # Se o valor do nó estiver no intervalo, imprimir
        if low <= node.value <= high:
            print(node.value, end=" ")

        # Se o valor do nó for menor que high, explorar a subárvore direita
        if node.value < high:
            self._find_interval(node.right, low, high)

    # ------ Questão 5 ------- 

    def print_tree(self):
        """Exibe a árvore em formato de árvore, mostrando valores, cores e pais"""
        if self.root == self.NIL:
            print("Árvore vazia.")
            return

        queue = deque()
        queue.append((self.root, None))  # Agora armazena (nó, pai)

        level = 0
        while queue:
            print(f"Nível {level}:", end=" ")
            level_size = len(queue)
            level_nodes = []

            for _ in range(level_size):
                node, parent = queue.popleft()
                
                # Formata a relação pai-filho
                parent_info = ""
                if parent is not None:
                    parent_info = f" ← {parent.value}"
                
                color = "V" if node.color == Color.RED else "P"
                level_nodes.append(f"{node.value} ({color}){parent_info}")

                # Adiciona filhos à fila com informação do pai
                if node.left != self.NIL:
                    queue.append((node.left, node))
                if node.right != self.NIL:
                    queue.append((node.right, node))

            print(" | ".join(level_nodes))
            level += 1