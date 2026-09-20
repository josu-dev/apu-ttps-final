"""
Trabajo Final - Algoritmos y Estructuras de Datos
Tema: Tries (Árboles de Prefijos)
Enfoque 3: Hibridación de Trie + Programación Dinámica (Optimización de Transiciones)

Problema: Word Combinations (CSES 1731 / similar a LeetCode 139 Word Break)
URL: https://cses.fi/problemset/task/1731/

Descripción:
Dada una cadena S de longitud N (N <= 5,000) y un diccionario de K palabras
(K <= 100,000, suma de longitudes <= 1,000,000), contar de cuántas formas se puede
formar la cadena S concatenando palabras del diccionario.
El resultado debe darse módulo 10^9 + 7.

Fundamento Teórico:
1. Formulación de la Programación Dinámica:
   Sea dp[i] la cantidad de formas de formar el sufijo S[i..N-1].
   Caso base: dp[N] = 1 (la cadena vacía se forma de 1 sola manera).
   Para calcular dp[i]:
   Buscamos todas las palabras W del diccionario que coincidan con un prefijo de S[i..N-1].
   Si S[i..i+|W|-1] == W, entonces dp[i] += dp[i + |W|].

2. Por qué el Trie es fundamental aquí:
   - Sin Trie: Para cada posición i, buscar en un hash set o comparar contra las K palabras
     costaría O(N * K * L) o O(N * L_max) con sobrecarga de substrings y hashing.
   - Con Trie: Insertamos todas las palabras del diccionario en el Trie.
     Para cada posición i (desde N-1 hasta 0):
     Descendemos por el Trie con S[i], S[i+1], S[i+2], ...
     - Si el carácter S[j] no tiene arista en el Trie, CORTAMOS EL BUCLE INMEDIATAMENTE (break).
       Ninguna palabra en el diccionario comienza con ese prefijo.
     - Si el nodo actual marca fin de palabra, encontramos una palabra válida W = S[i..j]:
       dp[i] = (dp[i] + dp[j+1]) % MOD.

Complejidad:
- Tiempo: O(Longitud total de palabras para construir el Trie + N * profundidad_efectiva).
  En la práctica, la poda del Trie descarta caminos inviables en los primeros 1 a 3 caracteres.
- Espacio: O(Total_caracteres_diccionario * 26) para los nodos del Trie, más O(N) para la tabla DP.
"""

import sys

MOD = 1_000_000_007


class TrieForDP:
    """
    Trie estructurado con arreglos planos para optimizar el acceso a memoria y la velocidad.
    Cada nodo contiene:
    - next_node: lista de tamaño 26 (para 'a'-'z')
    - is_end: booleano indicando si alguna palabra termina aquí
    """

    def __init__(self):
        # Usamos listas de enteros para minimizar overhead
        # nodo 0 = raíz
        self.next_node = [[0] * 26]
        self.is_end = [False]
        self.node_count = 1

    def insert(self, word: str) -> None:
        curr = 0
        for ch in word:
            c_idx = ord(ch) - 97  # ord('a') == 97
            nxt = self.next_node[curr][c_idx]
            if nxt == 0:
                nxt = self.node_count
                self.node_count += 1
                self.next_node.append([0] * 26)
                self.is_end.append(False)
                self.next_node[curr][c_idx] = nxt
            curr = nxt
        self.is_end[curr] = True


def count_word_combinations(target: str, words: list[str]) -> int:
    """
    Calcula el número de combinaciones de palabras para formar 'target' módulo 10^9 + 7.
    """
    n = len(target)
    if n == 0:
        return 1

    # 1. Construir el Trie con el diccionario de palabras
    trie = TrieForDP()
    for w in words:
        w = w.strip()
        if w:
            trie.insert(w)

    next_node = trie.next_node
    is_end = trie.is_end

    # Pre-convertir la cadena target a índices 0..25 para evitar llamadas a ord() repetidas
    target_indices = [ord(c) - 97 for c in target]

    # 2. Tabla DP: dp[i] = formas de formar target[i..n-1]
    dp = [0] * (n + 1)
    dp[n] = 1  # Caso base

    # 3. DP iterativa de derecha a izquierda
    for i in range(n - 1, -1, -1):
        curr_node = 0
        ways = 0
        for j in range(i, n):
            c_idx = target_indices[j]
            nxt = next_node[curr_node][c_idx]
            if nxt == 0:
                # Poda fundamental del Trie: ninguna palabra continúa con este prefijo
                break
            curr_node = nxt
            if is_end[curr_node]:
                ways += dp[j + 1]
                if ways >= MOD:
                    ways %= MOD

        dp[i] = ways

    return dp[0]


# ==============================================================================
# Casos de Prueba y Verificación
# ==============================================================================
def run_tests():
    print("=" * 60)
    print("Ejecutando pruebas para Enfoque 3: Trie + DP (CSES 1731)")
    print("=" * 60)

    # Caso 1 del enunciado oficial de CSES 1731
    # Target: "abaps"
    # Palabras: ["ab", "ba", "ps", "a", "b"]
    # Formas posibles:
    # 1) "ab" + "a" + "ps"
    # 2) "a" + "b" + "a" + "ps"
    # 3) "a" + "ba" + "ps"
    # Total = 3
    target1 = "abaps"
    words1 = ["ab", "ba", "ps", "a", "b"]
    res1 = count_word_combinations(target1, words1)
    print(f"Caso 1 ('{target1}'): Resultado = {res1} -> Esperado: 3")
    assert res1 == 3

    # Caso 2: Palabra imposible de formar
    target2 = "algo"
    words2 = ["al", "goa", "alg"]
    res2 = count_word_combinations(target2, words2)
    print(f"Caso 2 ('{target2}'): Resultado = {res2} -> Esperado: 0")
    assert res2 == 0

    # Caso 3: Letras repetidas con múltiples descomposiciones
    # Target: "aaaa"
    # Palabras: ["a", "aa"]
    # Formas:
    # a+a+a+a, aa+a+a, a+aa+a, a+a+aa, aa+aa -> Total: 5 (números de Fibonacci)
    target3 = "aaaa"
    words3 = ["a", "aa"]
    res3 = count_word_combinations(target3, words3)
    print(f"Caso 3 ('{target3}'): Resultado = {res3} -> Esperado: 5")
    assert res3 == 5

    # Caso 4: Una sola palabra idéntica al target
    target4 = "hola"
    words4 = ["hola"]
    res4 = count_word_combinations(target4, words4)
    print(f"Caso 4 ('{target4}'): Resultado = {res4} -> Esperado: 1")
    assert res4 == 1

    print("Todas las pruebas pasaron exitosamente.\n")


def main():
    if sys.stdin.isatty():
        run_tests()
        return

    input_data = sys.stdin.read().split()
    if not input_data:
        run_tests()
        return

    target = input_data[0]
    k = int(input_data[1])
    words = input_data[2:2 + k]
    ans = count_word_combinations(target, words)
    print(ans)


if __name__ == "__main__":
    main()
