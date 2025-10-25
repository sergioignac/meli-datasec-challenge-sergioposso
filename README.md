# Meli datasec Challenge

## Autor
**Sergio Ignacio Posso Alvarez**
Challenge técnico para el proceso **Sr Engineer - Data Security**

### Estructura del proyecto

meli-datasec-challenge-sergioposso
│
├── python
│   |
|   │   logging_config.py
|   │   solution_best_in_genre.py
|   │   solution_minesweeper.py
|   │   __init__.py
|   │   
|   │───logs
|   │       app.log
|   │       
|   │───tests
|   │   │   test_best_in_genre_integration.py
|   │   │   test_best_in_genre_unit.py
|   │   │   test_minesweeper.py
|   │   │   __init__.py
|   │   │   
|   │   └───__pycache__
|   │           test_minesweeper.cpython-314-pytest-8.2.0.pyc
|   │           __init__.cpython-314.pyc
|   │
|   └───__pycache__
|           logging_config.cpython-314.pyc
|           solution_minesweeper.cpython-314.pyc
|           __init__.cpython-314.pyc
├── sql
├── go
├── requirements.txt # Dependencias del entorno
├── .gitignore
└── README.md

## Reto 1 - Minesweeper (Python)

### Descripción

El reto consiste en identificar el número de minas adyacentes a cada celda en una matriz binaría, 
donde las minas estan representadas con 1, y el resultado final marca las minas con 9.

La solución desarrollada incluye

- Validación de estructura y valores de entrada.
- Manejo de excepciones controlado.
- Logging detallado con niveles `INFO`, `DEBUG` y `ERROR`.
- Pruebas unitarias con `pytest`.
- Documentación de cada función.
- Código estructurado bajo principios de arquitectura limpia.

### Ejecución (En consola)

1. Activar el entorno virtual:

```bash
venv\Scripts\activate
```

2. Ejecutar el script principal:

```bash
python python/solution_minesweeper.py
```

3. Ejecutar las pruebas unitarias:

```bash
pytest -v
```

## Ejemplo de ejecución

### Entrada

```python
demo_matrix = [
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 0],
]
```

### Salida esperada
```python
[
    [1, 9, 2],
    [2, 3, 9],
    [9, 2, 1]
]
```
## Extracto de Log (python/logs/app.log)

2025-10-24 20:37:50 [INFO] [__main__] Ejecución de prueba en modo standalone.
2025-10-24 20:37:50 [INFO] [__main__] Iniciando cálculo de minas para matriz de 3x3
2025-10-24 20:37:50 [INFO] [__main__] Resultado de la matriz calculada:
2025-10-24 20:37:50 [INFO] [__main__] [1, 9, 2]
2025-10-24 20:37:50 [INFO] [__main__] [2, 3, 9]
2025-10-24 20:37:50 [INFO] [__main__] [9, 2, 1]

El log evidencia la correcta ejecución, el seguimiento de flujo, y el control de eventos durante el proceso.

## Pruebas Unitarias

Las pruebas se encuentran en el archivo `python/tests/test_minesweeper.py`.

Casos validados:

- Caso base con matriz válida.
- Matriz con valores inválidos (error controlado).
- Filas con longitudes diferentes (error controlado).

Ejemplo:

```python
def test_basic_case():
    matrix = [
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0],
    ]
    expected = [
        [1, 9, 2],
        [2, 3, 9],
        [9, 2, 1],
    ]
    result = calculate_mines(matrix)
    assert result == expected
```

Todas las pruebas se ejecutan correctamente, validando el comportamiento esperado y el manejo de excepciones.

## Dependencias

- Python 3.10 o superior  
- pytest 8.2.0  
- requests 2.32.0  
- requests-mock 1.11.0  

Instalación:

```bash
pip install -r requirements.txt
```

## Reto 2 - REST API — Best TV Shows in Genre

### Descripción

Este módulo (`solution_best_in_genre.py`) implementa la función `bestInGenre(genre: str) -> str`, la cual consulta la API pública: 
https://jsonmock.hackerrank.com/api/tvseries
El objetivo es identificar la serie con **mayor calificación IMDB** (`imdb_rating`) dentro de un género específico.  
En caso de empate, retorna el nombre alfabéticamente menor.  

El proceso implementa:

- **Paginación completa** (`?page={num}`)
- **Normalización de géneros**
- **Validaciones y manejo de errores**
- **Logging centralizado** (nivel INFO y DEBUG)
- **Pruebas unitarias e integración**
- **Arquitectura limpia y modular**

### Ejecución manual

Para ejecutar la búsqueda del mejor show dentro de un género específico:

```bash
python python/solution_best_in_genre.py "Action"
```

El resultado se imprimirá en consola y se registrará en el archivo de logs:
python/logs/app.log

### Ejemplo de salida (ejecución real)

**Input:**
```
Action
```

**Salida esperada (según API Hackerrank):**
```
The 4 highest-rated shows in the Action genre are:
Game of Thrones — 9.3
Avatar: The Last Airbender — 9.2
Hagane no renkinjutsushi — 9.1
Shingeki no kyojin — 8.9
Highest rated show overall: Game of Thrones (9.3)
```

### Ejemplo adicional (género Romance)

**Input:**
```
Romance
```

**Salida esperada:**
```
The 4 highest-rated shows in the Romance genre are:
Friends — 8.9
Downton Abbey — 8.7
This Is Us — 8.7
Modern Family — 8.4
Highest rated show overall: Friends (8.9)
```

### Pruebas unitarias e integración

Se incluyen casos con datos **mockeados** y pruebas de integración reales contra el endpoint, verificando:

- Correcto manejo de empates.
- Paginación completa (20 páginas).
- Registro del top 4 en logs.
- Validaciones de entrada.

### Extracto de Log real (Action)

```
2025-10-25 12:38:18 [INFO] [python.solution_best_in_genre] The 4 highest-rated shows in the Action genre are:
2025-10-25 12:38:18 [INFO] [python.solution_best_in_genre] Game of Thrones — 9.3
2025-10-25 12:38:18 [INFO] [python.solution_best_in_genre] Avatar: The Last Airbender — 9.2
2025-10-25 12:38:18 [INFO] [python.solution_best_in_genre] Hagane no renkinjutsushi — 9.1
2025-10-25 12:38:18 [INFO] [python.solution_best_in_genre] Shingeki no kyojin — 8.9
2025-10-25 12:38:18 [INFO] [python.solution_best_in_genre] Highest rated show overall: Game of Thrones (9.3)
```

## Enfoque de Seguridad

- Validaciones estrictas sobre entradas de datos.
- Logging controlado para trazabilidad y auditoría.
- Manejo centralizado de excepciones.
- Principio de responsabilidad única aplicado a cada módulo.
- Cumplimiento de buenas prácticas de desarrollo seguro.

---

## Resultado Final

- Código funcional y modular.
- Arquitectura limpia y mantenible.
- Pruebas unitarias exitosas.
- Logging completo y verificable.
- Documentación clara y profesional.
