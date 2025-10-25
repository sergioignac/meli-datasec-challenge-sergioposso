"""
Pruebas unitarias para solution_minesweeper.py
Usa pytest.
"""

import pytest
from python.solution_minesweeper import calculate_mines, MINE_OUT


def test_basic_case():
    matrix = [
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0],
    ]
    expected = [
        [1, MINE_OUT, 2],
        [2, 3, MINE_OUT],
        [MINE_OUT, 2, 1],
    ]
    result = calculate_mines(matrix)
    assert result == expected


def test_invalid_values():
    with pytest.raises(ValueError):
        calculate_mines([[0, 2], [1, 0]])


def test_irregular_rows():
    with pytest.raises(ValueError):
        calculate_mines([[0, 1], [1, 0, 1]])
