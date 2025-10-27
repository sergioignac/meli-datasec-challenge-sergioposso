"""
solution_minesweeper.py
-----------------------
Solución al reto Minesweeper (parte 1 del challenge técnico).

Autor: Sergio Ignacio Posso Alvarez
Go Version: Python 3.14.0

Objetivo:
A partir de una matriz binaria (0 = celda vacía, 1 = mina),
retorna una nueva matriz donde cada celda indica el número
de minas adyacentes. Las minas se marcan con 9.

Incluye:
- Validaciones de entrada.
- Logging centralizado.
- Docstrings detallados.
- Arquitectura limpia y testeable.
"""

import sys
from pathlib import Path
from typing import List

# 🔧 Ajuste clave para que funcione tanto en pytest como en ejecución directa
sys.path.append(str(Path(__file__).resolve().parent))

from logging_config import setup_logger  # noqa: E402

logger = setup_logger(__name__)

MINE = 1
MINE_OUT = 9


def calculate_mines(matrix: List[List[int]]) -> List[List[int]]:
    """
    Calcula el número de minas adyacentes en cada celda.

    Args:
        matrix (List[List[int]]): Matriz 2D de 0 y 1 representando el campo minado.

    Returns:
        List[List[int]]: Nueva matriz con la cantidad de minas adyacentes o 9 donde hay mina.

    Raises:
        ValueError: Si la matriz está vacía, tiene filas irregulares o valores distintos de 0 y 1.
    """
    if not matrix or not all(isinstance(row, list) for row in matrix):
        logger.error("Entrada inválida: la matriz está vacía o no es una lista de listas.")
        raise ValueError("La matriz no puede estar vacía y debe ser una lista de listas.")

    row_length = len(matrix[0])
    for row in matrix:
        if len(row) != row_length:
            logger.error("Filas de diferente longitud detectadas.")
            raise ValueError("Todas las filas deben tener la misma longitud.")
        if any(cell not in (0, 1) for cell in row):
            logger.error("Valores no permitidos detectados: %s", row)
            raise ValueError("La matriz solo puede contener 0 y 1.")

    logger.info("Iniciando cálculo de minas para matriz de %dx%d", len(matrix), row_length)

    result = []
    for i, row in enumerate(matrix):
        result_row = []
        for j, cell in enumerate(row):
            if cell == MINE:
                result_row.append(MINE_OUT)
            else:
                count = _count_adjacent_mines(matrix, i, j)
                result_row.append(count)
            logger.debug("Celda (%d,%d) => %d", i, j, result_row[-1])
        result.append(result_row)

    logger.info("Resultado de la matriz calculada:")
    for row in result:
        logger.info(row)
    return result


def _count_adjacent_mines(matrix: List[List[int]], row: int, col: int) -> int:
    """
    Cuenta las minas adyacentes a una celda específica.

    Args:
        matrix (List[List[int]]): Matriz de entrada.
        row (int): Índice de fila.
        col (int): Índice de columna.

    Returns:
        int: Cantidad de minas alrededor de la celda.
    """
    count = 0
    rows, cols = len(matrix), len(matrix[0])
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col) and matrix[i][j] == MINE:
                count += 1
    return count


if __name__ == "__main__":
    demo_matrix = [
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0],
    ]
    logger.info("Ejecución de prueba en modo standalone.")
    result = calculate_mines(demo_matrix)
    for row in result:
        print(row)
