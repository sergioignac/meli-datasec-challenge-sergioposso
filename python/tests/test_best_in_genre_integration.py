"""
Prueba de integración real con la API pública de Hackerrank.
Marcada con @pytest.mark.integration para ejecución opcional.
"""

import pytest
from python.solution_best_in_genre import bestInGenre


@pytest.mark.integration
def test_integration_action_genre():
    """Valida que la función se ejecute correctamente con la API real."""
    res = bestInGenre("Action", timeout=10)
    # No comprobamos nombre exacto, ya que la API puede variar.
    # Validamos tipo de retorno y que no falle.
    assert res is None or isinstance(res, str)
