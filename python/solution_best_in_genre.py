"""
solution_best_in_genre.py
-------------------------
Busca la serie con mayor IMDB rating para un género dado,
usando la API pública: https://jsonmock.hackerrank.com/api/tvseries

Autor: Sergio Ignacio Posso Alvarez
Go Version: Python 3.14.0

Comportamiento:
- Pagina todos los resultados.
- Normaliza el campo `genre` (coma-separado).
- Si hay empate por rating, devuelve el nombre alfabéticamente menor.
- Registra eventos, errores y respuestas JSON en el logger central.
"""

import sys
import json
from pathlib import Path
from typing import Optional

# Permite ejecutar tanto como script directo como módulo en paquete
sys.path.append(str(Path(__file__).resolve().parent))

import requests  # noqa: E402
from logging_config import setup_logger  # noqa: E402

logger = setup_logger(__name__)

BASE_URL = "https://jsonmock.hackerrank.com/api/tvseries"


def _parse_genres(genre_field: str) -> list[str]:
    """
    Convierte el campo 'genre' (ej. "Action, Drama") en lista de géneros normalizados.
    """
    if not genre_field:
        return []
    return [g.strip().lower() for g in genre_field.split(",") if g.strip()]


def bestInGenre(genre: str, timeout: int = 10) -> Optional[str]:
    """
    Devuelve el nombre de la serie con mayor imdb_rating para el género dado.
    Si hay empate en rating, devuelve el nombre alfabéticamente menor.
    Retorna None si no se encuentra ninguna serie o si ocurre un error de red.

    Args:
        genre (str): género a buscar (p. ej. "Action")
        timeout (int): timeout en segundos para cada petición HTTP

    Returns:
        Optional[str]: nombre de la serie o None
    """
    if not genre or not isinstance(genre, str):
        logger.error("Argumento 'genre' inválido: %r", genre)
        raise ValueError("genre must be a non-empty string")

    target = genre.strip().lower()
    logger.info("Iniciando búsqueda para el género: %s", target)

    page = 1
    best_name: Optional[str] = None
    best_rating: float = float("-inf")

    all_matches = []  # <- lista para almacenar todas las coincidencias

    while True:
        try:
            url = f"{BASE_URL}?page={page}"
            logger.info("Solicitando página %s: %s", page, url)
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as exc:
            logger.error("Error al solicitar datos (página %s): %s", page, exc)
            return None
        except ValueError as exc:
            logger.error("Respuesta no JSON en página %s: %s", page, exc)
            return None

        items = data.get("data", [])
        for item in items:
            name = item.get("name")
            gfield = item.get("genre") or ""
            rating = item.get("imdb_rating")

            try:
                rating_val = float(rating) if rating is not None else float("-inf")
            except (TypeError, ValueError):
                rating_val = float("-inf")

            genres = _parse_genres(gfield)
            if target in genres:
                all_matches.append({"name": name, "rating": rating_val})
                if (rating_val > best_rating) or (rating_val == best_rating and (best_name is None or name < best_name)):
                    best_rating = rating_val
                    best_name = name

        total_pages = data.get("total_pages", 1)
        if page >= total_pages:
            break
        page += 1

    # Registrar el top 4
    if all_matches:
        top_sorted = sorted(all_matches, key=lambda x: (-x["rating"], x["name"]))[:4]
        logger.info("The 4 highest-rated shows in the %s genre are:", genre)
        for show in top_sorted:
            logger.info("%s — %.1f", show["name"], show["rating"])

    if best_name:
        logger.info("Highest rated show overall: %s (%.1f)", best_name, best_rating)
    else:
        logger.info("No se encontró serie para el género: %s", genre)

    return best_name


if __name__ == "__main__":
    import sys as _sys

    if len(_sys.argv) < 2:
        print("Uso: python solution_best_in_genre.py \"Action\"")
        _sys.exit(1)

    genre_input = _sys.argv[1]
    logger.info("Ejecución directa del módulo con parámetro: %s", genre_input)
    res = bestInGenre(genre_input)
    if res:
        print(f"Best in genre '{genre_input}': {res}")
    else:
        print("No result or error (check logs).")
