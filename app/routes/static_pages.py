"""
Rutas para servir archivos estáticos (el frontend).
Separado en su propio blueprint para mantener limpio
el blueprint de la API.
"""

from flask import Blueprint, send_from_directory, current_app

static_bp = Blueprint("static_pages", __name__)


@static_bp.route("/")
def index():
    """Sirve el frontend principal."""
    return send_from_directory(current_app.static_folder, "index.html")
