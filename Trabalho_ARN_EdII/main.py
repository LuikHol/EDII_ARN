from red_black_tree import RedBlackTree

def main():
    # Cria uma árvore rubro-negra vazia
    rbt = RedBlackTree()

    # 1 - Insira as chaves 5, 16, 22, 45, 2, 10, 18, 30, 50, 12, 1, nesta ordem.
    print("Inserindo chaves: 5, 16, 22, 45, 2, 10, 18, 30, 50, 12, 1")
    keys_to_insert = [5, 16, 22, 45, 2, 10, 18, 30, 50, 12, 1]
    for key in keys_to_insert:
        rbt.insert(key)
    print("Árvore após inserções:")
    rbt.print_tree()
    print()

    # 2 - Procure pelas chaves 22 e 15.
    print("Procurando pela chave 22:", "Encontrado" if rbt.find(22) else "Não encontrado")
    print("Procurando pela chave 15:", "Encontrado" if rbt.find(15) else "Não encontrado")
    print()

    # 3 - Exclua as chaves 30, 10 e 22, nesta ordem. Insira as chaves 25, 9, 33 e 50, nesta ordem.
    print("Excluindo chaves: 30, 10, 22")
    keys_to_delete = [30, 10, 22]
    for key in keys_to_delete:
        rbt.delete_by_val(key)
    print("Árvore após exclusões:")
    rbt.print_tree()
    print()

    print("Inserindo chaves: 25, 9, 33, 50")
    keys_to_insert = [25, 9, 33, 50]
    for key in keys_to_insert:
        rbt.insert(key)
    print("Árvore após inserções:")
    rbt.print_tree()
    print()

    # 4 - Encontre o maior, o menor e o quinto menor valor da árvore.
    print("Maior valor da árvore:", rbt.find_max())
    print("Menor valor da árvore:", rbt.find_min())
    print("Quinto menor valor da árvore:", rbt.find_kth(5))
    print()

    # 5 - Encontre todos os elementos entre 10 e 30.
    print("Elementos no intervalo [10, 30]:")
    rbt.find_interval(10, 30)
    print()

# Executa a função main
if __name__ == "__main__":
    main()