import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(name: str = "meli_logger") -> logging.Logger:
    """Configura y retorna un logger con salida a archivo y consola."""
    logs_dir = Path(__file__).resolve().parent / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_file = logs_dir / "app.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Evita duplicar handlers si ya se configuró antes
    if logger.handlers:
        return logger

    # Formato estándar
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler para archivo (rotación 5MB)
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=2)
    file_handler.setFormatter(formatter)

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("Logger configurado correctamente. Archivo de log: %s", log_file)
    return logger


if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Prueba inicial de logging exitosa.")
