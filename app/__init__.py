"""
App Factory.
Crea y configura la instancia de Flask.
Usar create_app() en lugar de instanciar Flask directamente
permite tener múltiples configuraciones (dev, prod, testing) sin conflictos.
"""

import logging
import os
from pathlib import Path
from flask import Flask

from config import Config


def create_app(config: Config) -> Flask:
    """
    Factory que construye y retorna la app Flask configurada.

    Args:
        config: Objeto de configuración (Dev, Prod, Testing).

    Returns:
        Instancia de Flask lista para correr.
    """
    project_root = Path(__file__).resolve().parent.parent
    static_path = project_root / "static"

    app = Flask(__name__, static_folder=str(static_path))
    app.config.from_object(config)

    _setup_logging(config)
    _register_blueprints(app)

    return app


def _setup_logging(config: Config) -> None:
    """Configura el sistema de logging de la aplicación."""
    level = logging.DEBUG if config.DEBUG else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _register_blueprints(app: Flask) -> None:
    """Registra todos los blueprints (grupos de rutas) de la app."""
    from app.routes.calculator import calculator_bp
    from app.routes.static_pages import static_bp

    app.register_blueprint(static_bp)
    app.register_blueprint(calculator_bp, url_prefix="/api")
