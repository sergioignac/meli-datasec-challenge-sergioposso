"""
Pruebas unitarias para solution_best_in_genre.py
Usan requests-mock para simular respuestas HTTP.
"""

import requests_mock
import logging
from python.solution_best_in_genre import bestInGenre

# Configurar logging para capturar mensajes durante los tests
logging.basicConfig(level=logging.INFO)


def _make_response(page, total_pages, items):
    """Simula una respuesta de la API paginada."""
    return {
        "page": page,
        "per_page": len(items),
        "total": len(items) * total_pages,
        "total_pages": total_pages,
        "data": items,
    }


def test_best_in_genre_single_page():
    """Debe retornar la serie con mayor rating."""
    with requests_mock.Mocker() as m:
        items = [
            {"name": "Show A", "genre": "Action, Drama", "imdb_rating": 8.5},
            {"name": "Show B", "genre": "Action", "imdb_rating": 9.0},
            {"name": "Show C", "genre": "Comedy", "imdb_rating": 9.5},
        ]
        m.get("https://jsonmock.hackerrank.com/api/tvseries?page=1", json=_make_response(1, 1, items))
        result = bestInGenre("Action")
        assert result == "Show B"


def test_best_in_genre_tiebreaker():
    """Debe aplicar desempate alfabético cuando dos tienen mismo rating."""
    with requests_mock.Mocker() as m:
        items = [
            {"name": "Beta", "genre": "Action", "imdb_rating": 9.0},
            {"name": "Alpha", "genre": "Action", "imdb_rating": 9.0},
        ]
        m.get("https://jsonmock.hackerrank.com/api/tvseries?page=1", json=_make_response(1, 1, items))
        result = bestInGenre("Action")
        assert result == "Alpha"


def test_best_in_genre_invalid_input():
    """Debe lanzar ValueError si el argumento es inválido."""
    try:
        bestInGenre(None)
    except ValueError:
        assert True
    else:
        assert False


def test_best_in_genre_logging_top4(tmp_path, caplog):
    """
    Verifica que el log incluya la línea 'The 4 highest-rated shows...'
    y los nombres de las series.
    """
    with requests_mock.Mocker() as m:
        items = [
            {"name": "A", "genre": "Action", "imdb_rating": 9.3},
            {"name": "B", "genre": "Action", "imdb_rating": 9.2},
            {"name": "C", "genre": "Action", "imdb_rating": 9.1},
            {"name": "D", "genre": "Action", "imdb_rating": 8.9},
            {"name": "E", "genre": "Action", "imdb_rating": 8.8},
        ]
        m.get("https://jsonmock.hackerrank.com/api/tvseries?page=1", json=_make_response(1, 1, items))
        with caplog.at_level(logging.INFO):
            result = bestInGenre("Action")

        assert result == "A"
        assert "The 4 highest-rated shows in the Action genre are:" in caplog.text
        assert "A — 9.3" in caplog.text
        assert "D — 8.9" in caplog.text
