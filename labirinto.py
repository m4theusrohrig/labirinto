import heapq
from collections import deque

# I = início, F = fim, # = parede, . = casa livre
labirinto = [
    "I...#.....",
    ".##.#.###.",
    "....#...#.",
    ".####.#.#.",
    "......#...",
    ".######.#.",
    "...#....#.",
    "##.#.####.",
    "...#.....F",
    ".#.#######",
]

DIRECOES = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # cima, direita, baixo, esquerda


def achar(lab, simbolo):
    for i, linha in enumerate(lab):
        if simbolo in linha:
            return (i, linha.index(simbolo))


def livre(lab, i, j):
    dentro = 0 <= i < len(lab) and 0 <= j < len(lab[0])
    return dentro and lab[i][j] != '#'


def montar_grafo(lab):
    grafo = {}
    for i in range(len(lab)):
        for j in range(len(lab[0])):
            if not livre(lab, i, j):
                continue
            grafo[(i, j)] = []
            for di, dj in DIRECOES:
                if livre(lab, i + di, j + dj):
                    grafo[(i, j)].append((i + di, j + dj))
    return grafo


def reconstruir(pai, inicio, saida):
    caminho = [saida]
    while caminho[-1] != inicio:
        caminho.append(pai[caminho[-1]])
    caminho.reverse()
    return caminho


def dfs(grafo, inicio, saida):
    pai = {}
    visitados = set()

    def visitar(v):
        visitados.add(v)
        if v == saida:
            return True
        for w in grafo[v]:
            if w not in visitados:
                pai[w] = v
                if visitar(w):
                    return True
        return False

    visitar(inicio)
    return reconstruir(pai, inicio, saida), len(visitados)


def bfs(grafo, inicio, saida):
    pai = {}
    visitados = {inicio}
    fila = deque([inicio])
    expandidas = 0
    while fila:
        v = fila.popleft()
        expandidas += 1
        if v == saida:
            break
        for w in grafo[v]:
            if w not in visitados:
                visitados.add(w)
                pai[w] = v
                fila.append(w)
    return reconstruir(pai, inicio, saida), expandidas


def h(v, saida):  # distância de Manhattan
    return abs(v[0] - saida[0]) + abs(v[1] - saida[1])


def gulosa(grafo, inicio, saida):
    pai = {}
    visitados = {inicio}
    fronteira = [(h(inicio, saida), inicio)]
    expandidas = 0
    while fronteira:
        _, v = heapq.heappop(fronteira)
        expandidas += 1
        if v == saida:
            break
        for w in grafo[v]:
            if w not in visitados:
                visitados.add(w)
                pai[w] = v
                heapq.heappush(fronteira, (h(w, saida), w))
    return reconstruir(pai, inicio, saida), expandidas


def desenhar(lab, caminho):
    grade = [list(linha) for linha in lab]
    for i, j in caminho:
        if grade[i][j] == '.':
            grade[i][j] = '*'
    for linha in grade:
        print(''.join(linha))


if __name__ == "__main__":
    inicio = achar(labirinto, 'I')
    saida = achar(labirinto, 'F')
    grafo = montar_grafo(labirinto)

    resultados = {}
    for nome, busca in [("DFS", dfs), ("BFS", bfs), ("Gulosa", gulosa)]:
        caminho, visitadas = busca(grafo, inicio, saida)
        resultados[nome] = (len(caminho) - 1, visitadas)
        print(f"\n{nome}: caminho com {len(caminho) - 1} passos, {visitadas} casas visitadas")
        desenhar(labirinto, caminho)

    print("\n| Algoritmo | Tamanho do caminho (passos) | Casas visitadas |")
    print("|-----------|-----------------------------|-----------------|")
    for nome, (tam, vis) in resultados.items():
        print(f"| {nome} | {tam} | {vis} |")
