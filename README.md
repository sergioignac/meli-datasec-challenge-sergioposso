# Meli datasec Challenge

## Autor
**Sergio Ignacio Posso Alvarez**
Challenge técnico para el proceso **Sr Engineer - Data Security**

### Entornos de desarrollo

- **Go:** 1.25.3 windows/amd64  
- **Python:** 3.14.0

### Estructura del proyecto

meli-datasec-challenge-sergioposso/
│
├── python/                                 # Soluciones en Python (Reto 1 y Reto 2)
│   │
│   ├── logging_config.py                   # Configuración centralizada de logs
│   ├── solution_best_in_genre.py           # Reto 2 - Best TV Shows in Genre (API REST)
│   ├── solution_minesweeper.py             # Reto 1 - Minesweeper (lógica y ejecución)
│   └── __init__.py                         # Inicialización del paquete Python
│
│   ├── logs/
│   │   └── app.log                         # Archivo de log general de ejecución
│   │
│   └── tests/                              # Pruebas unitarias e integración
│       ├── test_best_in_genre_integration.py
│       ├── test_best_in_genre_unit.py
│       ├── test_minesweeper.py
│       └── __init__.py
│
├── sql/                                    # Reto 3 - Consultas SQL
│   └── solution_failures_report.sql        # Query de reporte de fallos publicitarios
│
├── challenge_go/                           # Reto 4 - CLI en Go (Text Summarizer)
│   ├── solution_summarizer.go              # CLI que resume texto usando HuggingFace API
│   ├── solution_summarizer_test.go         # Pruebas del CLI
│   ├── article.txt                         # Archivo de ejemplo para prueba de resumen
│   ├── go.mod                              # Archivo de módulo Go
│   └── logs/
│       └── app.log                         # Log del CLI (ejecuciones y errores)
│
├── requirements.txt                        # Dependencias de entorno Python
├── .gitignore                              # Exclusiones de control de versiones
└── README.md                               # Documentación completa del challenge


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
```
2025-10-24 20:37:50 [INFO] [__main__] Ejecución de prueba en modo standalone.
2025-10-24 20:37:50 [INFO] [__main__] Iniciando cálculo de minas para matriz de 3x3
2025-10-24 20:37:50 [INFO] [__main__] Resultado de la matriz calculada:
2025-10-24 20:37:50 [INFO] [__main__] [1, 9, 2]
2025-10-24 20:37:50 [INFO] [__main__] [2, 3, 9]
2025-10-24 20:37:50 [INFO] [__main__] [9, 2, 1]
```

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

## Reto 3 - SQL: Advertising System Failures Report

### Descripción

Este reto tiene como objetivo identificar los **clientes con más de 3 eventos de fallo (`status = 'failure'`)** en sus campañas publicitarias, dentro del sistema de analítica de HackerAd.  
El resultado debe mostrar el **nombre completo del cliente** y el **número total de fallos** detectados en sus campañas, ordenado de mayor a menor número de fallos, y alfabéticamente en caso de empate.

El query fue desarrollado en el archivo: **sql/solution_failures_report.sql**

Genera un reporte de clientes con más de 3 eventos de fallo (`status = 'failure'`)
en sus campañas de publicidad, consolidando los datos de las tablas customers, campaigns y events.

Comportamiento:
- Agrupa los eventos por cliente.
- Filtra únicamente los registros con estado 'failure'.
- Retorna solo los clientes con más de tres fallos.
- Ordena los resultados por cantidad de fallos (descendente) y nombre del cliente (ascendente).

## Resultado esperado

 **customer**            **failures**
Whitney Ferrero               6

| customer                                   | failures |
|--------------------------------------------|----------|
| Whitney Ferrero                            |    6     |

## Reto 4 - Go CLI: Text Summarizer with GenAI

### Descripción 

Este módulo implementa un CLI desarrollado en Go que permite resumir el contenido de un archivo de texto local utilizando un modelo público de Inteligencia Artificial Generativa (GenAI) a través de la HuggingFace Inference API.

El programa lee el contenido de un archivo .txt, lo envía al modelo facebook/bart-large-cnn y muestra en consola un resumen según el tipo solicitado por el usuario.

El código está diseñado siguiendo buenas prácticas de seguridad, manejo de errores y registro de logs, para garantizar trazabilidad y uso seguro de credenciales.

### Estructura del módulo

challenge_go/
├── solution_summarizer.go           # Implementación principal del CLI
├── solution_summarizer_test.go      # Pruebas unitarias básicas
├── article.txt                      # Archivo de prueba
├── go.mod                           # Archivo de configuración del módulo Go
└── logs/
    └── app.log                      # Registro local de ejecución

### Requisitos previos

1. Go 1.25 o superior
2. Conexión a Internet (para acceder a la API pública de HuggingFace)
3. Token personal de acceso gratuito a HuggingFace

### Autenticación (Importante)

Este proyecto utiliza la API pública de **HuggingFace Inference API** con el modelo:
[`facebook/bart-large-cnn`](https://huggingface.co/facebook/bart-large-cnn)

Para ejecutar correctamente el CLI, se requiere un token personal de HuggingFace.

1. Crear una cuenta gratuita en HuggingFace: https://huggingface.co
2. Ir a *Settings → Access Tokens* y generar un token de tipo `read`.
3. Configurar la variable de entorno antes de ejecutar el comando:

#### En PowerShell (Windows):
```powershell
$env:HUGGINGFACE_TOKEN="hf_tuTokenAqui"
go run solution_summarizer.go --input article.txt --type bullet
```

#### En Bash / Zsh (macOS / Linux):
```bash
export HUGGINGFACE_TOKEN="hf_tuTokenAqui"
go run solution_summarizer.go --input article.txt --type bullet
```

Nota: No se incluye ningún token en este repositorio por motivos de seguridad.
Cada usuario debe configurar su propio token de lectura gratuito para ejecutar las pruebas.

### Ejemplos de uso

```bash
go run solution_summarizer.go --input article.txt --type short
go run solution_summarizer.go --input article.txt --type medium
go run solution_summarizer.go --input article.txt --type bullet
go run solution_summarizer.go -t short article.txt
```

### Tipos de resumen

| Tipo   | Descripción                                   | Longitud aproximada |
|--------|-----------------------------------------------|---------------------|
| short  | Resumen conciso de 1 a 2 frases               | 20 - 60 palabras    |
| medium | Párrafo descriptivo más detallado             | 80 - 150 palabras   |
| bullet | Lista de puntos clave extraídos del contenido | 100 - 250 palabras  |

### Pruebas (solution_summarizer_test.go)
El archivo de prueba valida los siguientes aspectos:
- Generación correcta del prompt (BuildPrompt)
- Validación de tipos de resumen (short, medium, bullet)
- Comportamiento ante tipos inválidos
- Inicialización del logger y estructura de logs
Ejecutar las pruebas desde la carpeta challenge_go:
```bash
cd challenge_go
go test -v
```

### Manejo de errores
El CLI implementa validaciones y manejo de errores para:
- Archivos inexistentes o vacíos.
- Argumentos incorrectos.
- Errores de red o de autenticación en la API.
- Tipos de resumen no válidos.
- Falta de token en las variables de entorno.
Todos los eventos y errores se registran en el archivo: logs/app.log

---

## Enfoque de Seguridad

- Validaciones estrictas sobre entradas de datos.
- Logging controlado para trazabilidad y auditoría.
- Manejo centralizado de excepciones.
- Principio de responsabilidad única aplicado a cada módulo.
- Cumplimiento de buenas prácticas de desarrollo seguro.

Este enfoque garantiza que las soluciones sean seguras, auditables y alineadas con las buenas prácticas 
de ingeniería de software y ciberseguridad aplicadas en entornos corporativos.

---

## Resultado Final

- Código funcional y modular.
- Arquitectura limpia y mantenible.
- Pruebas unitarias exitosas.
- Logging completo y verificable.
- Documentación clara y profesional.

---

## Licencia

Este repositorio se publica únicamente con fines de evaluación técnica. 
No se permite su uso comercial ni la redistribución sin autorización del autor.