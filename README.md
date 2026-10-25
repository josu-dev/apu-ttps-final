# Trabajo Final: Tries (Árboles de Prefijos) y Optimización de Consultas en Cadenas

**Materia:** Algoritmos y Estructuras de Datos  
**Tema:** Tries (Árboles de Prefijos) y Optimización de Consultas  
**Lenguaje:** Python 3 (Optimizado)  

---

## 📌 Descripción del Proyecto

Este trabajo final aborda una estructura de datos y técnica algorítmica **no vista durante la cursada**: los **Tries (Árboles de Prefijos)**.

El objetivo central es demostrar la versatilidad del Trie más allá de su uso típico como "diccionario de texto", aplicándolo a **4 problemas con enfoques y dominios conceptualmente diferentes**:
1. **Enfoque 1 (Texto y Prefijos):** Detección de prefijos conflictivos y consistencia en tiempo real (*Online*).
2. **Enfoque 2 (Dominio Numérico / Álgebra Booleana):** Bitwise Trie para consultas voraces (*Greedy*) de Máximo XOR de subarreglos.
3. **Enfoque 3 (Hibridación con Programación Dinámica):** Aceleración y poda radical de transiciones de DP para conteo y particionado de palabras.
4. **Enfoque 4 (Poda de Búsqueda Combinatoria):** Reducción del espacio de búsqueda en algoritmos de Backtracking / DFS sobre grillas 2D.

---

## 📁 Estructura del Repositorio

```text
final/
├── 01_phone_list.py          # Enfoque 1: UVa 11362 - Phone List (Prefijos y consistencia)
├── 02_max_xor_subarray.py    # Enfoque 2: CSES 1655 - Maximum XOR Subarray (Bitwise Trie)
├── 03_word_combinations.py   # Enfoque 3: CSES 1731 - Word Combinations (Trie + DP)
├── 04_playing_boggle.py      # Enfoque 4: UVa 11283 - Playing Boggle (Trie + Backtracking 2D)
├── index.html                # Presentación interactiva Reveal.js (animaciones y trazas)
├── dev.py                    # Servidor local de desarrollo con Hot-Reload
├── generate_qrs.py           # Generador de códigos QR vectoriales (ISO/IEC 18004)
├── qr_presentation.svg       # QR hacia la presentación online (GitHub Pages)
├── qr_repo.svg               # QR hacia el repositorio GitHub
├── README.md                 # Documentación general del proyecto
├── .gitignore                # Archivos ignorados por Git
└── .github/
    └── workflows/
        └── deploy-pages.yml  # Pipeline CI/CD para GitHub Pages
```

---

## 🚀 Cómo Ejecutar las Pruebas

Con `uv` instalado, cada script incluye una suite de casos de prueba que se ejecutan automáticamente al correr el archivo:

```bash
# 1. Probar Phone List (Enfoque 1)
uv run 01_phone_list.py

# 2. Probar Bitwise Trie (Enfoque 2)
uv run 02_max_xor_subarray.py

# 3. Probar Trie + DP (Enfoque 3)
uv run 03_word_combinations.py

# 4. Probar Boggle / Backtracking (Enfoque 4)
uv run 04_playing_boggle.py
```

---

## 🧠 Resumen de Enfoques y Complejidades

| Enfoque | Archivo | Problema | Complejidad Tradicional | Complejidad con Trie | Aporte Conceptual |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. Prefijos y Consistencia** | `01_phone_list.py` | UVa 11362 | $O(N^2 \cdot L)$ (Fuerza bruta) | **$O(\sum \|S_i\|)$** | Detección *online* de prefijos durante la inserción en una sola pasada. |
| **2. Bitwise Trie (XOR)** | `02_max_xor_subarray.py` | CSES 1655 | $O(N^2)$ (Pares de prefijos) | **$O(N \cdot 30)$** | Extensión del Trie a cadenas de bits y decisiones Greedy bit a bit. |
| **3. Trie + DP** | `03_word_combinations.py` | CSES 1731 | $O(N \cdot K \cdot L)$ | **$O(N \cdot \text{prof.})$** | Poda inmediata de transiciones de DP al no hallar prefijos válidos. |
| **4. Poda en Backtracking** | `04_playing_boggle.py` | UVa 11283 | $O(M \cdot 16 \cdot 8^L)$ | **$O(16 \cdot 8^{\text{podado}})$** | Descarte instantáneo de ramas infructuosas en búsqueda 2D y poda dinámica de hojas del Trie. |

---

## 📊 Presentación Interactiva (Reveal.js)

El proyecto incluye una presentación web interactiva desarrollada con **Reveal.js**, fórmulas matemáticas en **KaTeX**, animaciones paso a paso de algoritmos (*Aho-Corasick*, construcción de Tries) y referencias directas al código fuente:

- **Ver online:** [https://josu-dev.github.io/apu-ttps-final](https://josu-dev.github.io/apu-ttps-final)
- **Ejecutar localmente con Hot-Reload:**
  ```bash
  uv run dev.py
  ```
  Abre automáticamente la presentación en `http://localhost:8000/index.html` con recarga instantánea al guardar cambios.
