"""
Trabajo Final - Algoritmos y Estructuras de Datos
Tema: Tries (Árboles de Prefijos)
Enfoque 1: Propiedades de Prefijos y Consistencia en Tiempo Real

Problema: UVa 11362 - Phone List (también SPOJ - PHONELST)
URL: https://vjudge.net/problem/UVA-11362

Descripción:
Dado un conjunto de números de teléfono, determinar si la lista es consistente.
Una lista es consistente si NINGÚN número es prefijo de otro. Por ejemplo:
- "911" y "97625999" -> Consistente
- "911" y "91125426" -> Inconsistente (911 es prefijo de 91125426)

Por qué este enfoque:
Muestra la propiedad fundamental del Trie: detección inmediata de prefijos en tiempo
de inserción en O(L) por palabra (donde L es la longitud del número), sin necesidad
de ordenar las cadenas ni realizar comparaciones cuadráticas O(N^2 * L).
"""

import sys


class TrieNode:
    """
    Representación de un nodo en el Trie.
    Optimizada con __slots__ para minimizar el overhead de memoria en Python.
    """
    __slots__ = ('children', 'is_end')

    def __init__(self):
        # Usamos diccionario para los hijos (dígitos '0'-'9')
        # En alfabetos fijos pequeños, dict o lista de tamaño 10 tienen excelente rendimiento.
        self.children = {}
        self.is_end = False


class PhoneListTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert_and_check(self, phone: str) -> bool:
        """
        Inserta un número telefónico en el Trie y verifica simultáneamente
        si viola la propiedad de consistencia de prefijos.

        Retorna:
            False si se detecta que 'phone' es prefijo de otro número O si otro
                  número previo es prefijo de 'phone'.
            True si no hay conflicto de prefijo.
        """
        curr = self.root
        created_new_node = False

        for ch in phone:
            # Caso 1: Si pasamos por un nodo que ya es fin de palabra previa,
            # significa que un número anterior más corto es prefijo de 'phone'.
            if curr.is_end:
                return False

            if ch not in curr.children:
                curr.children[ch] = TrieNode()
                created_new_node = True

            curr = curr.children[ch]

        # Caso 2: Si ya era fin de palabra (duplicado exacto)
        if curr.is_end:
            return False

        # Caso 3: Si no creamos ningún nodo nuevo a lo largo de todo el camino,
        # significa que 'phone' es un prefijo de algún número más largo ya insertado.
        if not created_new_node:
            return False

        curr.is_end = True
        return True


def solve_phone_list(numbers: list[str]) -> bool:
    """
    Determina si la lista de números es consistente.
    Retorna True si es consistente ("YES"), False si no ("NO").
    """
    trie = PhoneListTrie()
    for num in numbers:
        num = num.strip()
        if not num:
            continue
        if not trie.insert_and_check(num):
            return False
    return True


# ==============================================================================
# Casos de Prueba y Verificación
# ==============================================================================
def run_tests():
    print("=" * 60)
    print("Ejecutando pruebas para Enfoque 1: Phone List (UVa 11362)")
    print("=" * 60)

    # Caso 1 del enunciado oficial
    case1 = ["911", "97625999", "91125426"]
    res1 = solve_phone_list(case1)
    print(f"Caso 1 (Prefijo existente al final): {'YES' if res1 else 'NO'} -> Esperado: NO")
    assert res1 is False

    # Caso 2 del enunciado oficial
    case2 = ["113", "12340", "123440", "12345", "98346"]
    res2 = solve_phone_list(case2)
    print(f"Caso 2 (Todos independientes): {'YES' if res2 else 'NO'} -> Esperado: YES")
    assert res2 is True

    # Caso 3: Prefijo insertado después del número más largo
    case3 = ["91125426", "97625999", "911"]
    res3 = solve_phone_list(case3)
    print(f"Caso 3 (Prefijo insertado después): {'YES' if res3 else 'NO'} -> Esperado: NO")
    assert res3 is False

    # Caso 4: Números idénticos
    case4 = ["123", "123"]
    res4 = solve_phone_list(case4)
    print(f"Caso 4 (Números idénticos): {'YES' if res4 else 'NO'} -> Esperado: NO")
    assert res4 is False

    print("Todas las pruebas pasaron exitosamente.\n")


def main():
    # Si se invoca sin argumentos en stdin o interactivamente, corre los tests
    if sys.stdin.isatty():
        run_tests()
        return

    input_data = sys.stdin.read().split()
    if not input_data:
        run_tests()
        return

    it = iter(input_data)
    num_test_cases = int(next(it))

    for _ in range(num_test_cases):
        n = int(next(it))
        numbers = [next(it) for _ in range(n)]
        consistent = solve_phone_list(numbers)
        print("YES" if consistent else "NO")


if __name__ == "__main__":
    main()
