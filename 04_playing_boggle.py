"""
Trabajo Final - Algoritmos y Estructuras de Datos
Tema: Tries (Árboles de Prefijos)
Enfoque 4: Poda de Búsqueda Combinatoria en Grillas 2D (Trie + Backtracking)

Problema: UVa 11283 - Playing Boggle (y LeetCode 212 Word Search II)
URL: https://vjudge.net/problem/UVA-11283

Descripción:
Dado un tablero de 4x4 con letras mayúsculas y una lista de M palabras,
determinar cuáles palabras pueden formarse en el tablero.
Reglas:
- Una palabra se forma comenzando en cualquier celda y moviéndose a celdas adyacentes
  (en las 8 direcciones: horizontal, vertical y diagonal).
- Cada celda del tablero puede usarse a lo sumo una vez por cada palabra.
- Puntuación según longitud de palabra:
    Longitud 3 o 4: 1 punto
    Longitud 5:     2 puntos
    Longitud 6:     3 puntos
    Longitud 7:     5 puntos
    Longitud >= 8:  11 puntos
    (Longitud < 3:  0 puntos)

Fundamento Teórico:
1. El problema de la explosión combinatoria:
   El espacio de búsqueda de caminos sin ciclos en una grilla de 4x4 con 8 direcciones
   crece a razón de 16 * 8^(L-1). Para L = 8, 8^7 es más de 2 millones de caminos por celda.
   Si buscamos M palabras individualmente, el costo se multiplica por M.

2. Por qué el Trie es revolucionario aquí (Poda de Espacio de Estados):
   En lugar de buscar cada palabra por separado, indexamos TODO el diccionario en un Trie.
   Luego, realizamos un único recorrido DFS en la grilla desde cada celda (r, c),
   avanzando simultáneamente en el tablero y en el Trie:
   - Si una celda adyacente contiene una letra que NO es hija del nodo actual del Trie,
     CORTAMOS LA RAMA DEL DFS INMEDIATAMENTE (PODA).
   - Miles de caminos sin sentido se descartan en los primeros 2 o 3 pasos.
   - Si alcanzamos un nodo que marca fin de palabra, registramos la palabra como encontrada
     y continuamos explorando por si es prefijo de otra más larga.

Complejidad:
- Tiempo: O(Construcción_Trie + 16 * Factor_de_ramificación_podado).
  En la práctica corre en milisegundos incluso para diccionarios grandes.
- Espacio: O(Total_caracteres_diccionario) para el Trie y O(1) memoria auxiliar (grilla 4x4 fija).
"""

import sys

# Puntuación oficial de Boggle según longitud
SCORES = {
    1: 0,
    2: 0,
    3: 1,
    4: 1,
    5: 2,
    6: 3,
    7: 5,
}

# 8 direcciones posibles (horizontal, vertical, diagonal)
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]


class BoggleTrieNode:
    __slots__ = ('children', 'word_index')

    def __init__(self):
        self.children = {}
        # Guardamos el índice de la palabra original para marcarla como encontrada rápidamente
        self.word_index = -1


class BoggleTrie:
    def __init__(self):
        self.root = BoggleTrieNode()

    def insert(self, word: str, index: int) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = BoggleTrieNode()
            curr = curr.children[ch]
        curr.word_index = index


def solve_boggle_board(grid: list[str], words: list[str]) -> tuple[int, set[int]]:
    """
    Resuelve el juego de Boggle para una grilla de 4x4 y una lista de palabras.

    Retorna:
        - total_score: puntuación acumulada de las palabras válidas encontradas.
        - found_indices: conjunto con los índices de las palabras halladas.
    """
    # 1. Insertar todas las palabras en el Trie
    trie = BoggleTrie()
    for idx, w in enumerate(words):
        trie.insert(w, idx)

    found_word_indices = set()
    rows, cols = 4, 4
    visited = [[False] * cols for _ in range(rows)]

    def dfs(r: int, c: int, trie_node: BoggleTrieNode):
        ch = grid[r][c]
        if ch not in trie_node.children:
            # PODA: Ninguna palabra del diccionario continúa con este camino
            return

        next_node = trie_node.children[ch]

        # Si este nodo completa una palabra del diccionario
        if next_node.word_index != -1:
            found_word_indices.add(next_node.word_index)
            # Nota: No retornamos aquí porque la palabra actual podría ser
            # prefijo de una palabra aún más larga (ej. "CAT" y "CATER").

        visited[r][c] = True

        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                dfs(nr, nc, next_node)

        visited[r][c] = False  # Backtrack

    # Iniciar DFS desde cada una de las 16 posiciones del tablero
    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie.root)

    # Calcular puntaje total
    total_score = 0
    for idx in found_word_indices:
        length = len(words[idx])
        score = SCORES.get(length, 11 if length >= 8 else 0)
        total_score += score

    return total_score, found_word_indices


# ==============================================================================
# Casos de Prueba y Verificación
# ==============================================================================
def run_tests():
    print("=" * 60)
    print("Ejecutando pruebas para Enfoque 4: Boggle / Trie + DFS (UVa 11283)")
    print("=" * 60)

    # Tablero de ejemplo
    # T N E I
    # A I N T
    # E S P O
    # N I N E
    grid1 = [
        "TNEI",
        "AINT",
        "ESPO",
        "NINE"
    ]
    words1 = [
        "NINE",       # len 4 -> 1 pt (fila 3)
        "POINT",      # len 5 -> 2 pts
        "SEASONS",    # len 7
        "PAINT",      # len 5 -> 2 pts
        "TENTS",      # len 5
        "NONEXIST"    # no está en el tablero
    ]

    score, found = solve_boggle_board(grid1, words1)
    found_words = [words1[i] for i in found]
    print(f"Palabras encontradas en el tablero: {found_words}")
    print(f"Puntaje total obtenido: {score}")

    assert "NINE" in found_words
    assert "NONEXIST" not in found_words
    assert score > 0

    # Caso 2: Tablero donde una palabra es prefijo de otra
    grid2 = [
        "CATO",
        "XXXX",
        "XXXX",
        "XXXX"
    ]
    words2 = ["CAT", "CATO", "DOG"]
    score2, found2 = solve_boggle_board(grid2, words2)
    found_words2 = [words2[i] for i in found2]
    print(f"\nCaso 2 (Prefijos en grilla): {found_words2}")
    assert "CAT" in found_words2
    assert "CATO" in found_words2
    assert "DOG" not in found_words2

    print("Todas las pruebas pasaron exitosamente.\n")


def main():
    if sys.stdin.isatty():
        run_tests()
        return

    input_data = sys.stdin.read().split()
    if not input_data:
        run_tests()
        return

    it = iter(input_data)
    num_games = int(next(it))

    for game_idx in range(1, num_games + 1):
        grid = [next(it) for _ in range(4)]
        m = int(next(it))
        words = [next(it) for _ in range(m)]
        score, _ = solve_boggle_board(grid, words)
        print(f"Score for Boggle game #{game_idx}: {score}")


if __name__ == "__main__":
    main()
