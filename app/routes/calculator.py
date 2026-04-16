"""
Rutas de la API de la calculadora.

Este archivo SOLO maneja HTTP:
  - Leer el request
  - Llamar al servicio correspondiente
  - Retornar la respuesta JSON

No hay lógica de negocio aquí. Si una ruta crece demasiado,
es señal de que algo debe moverse al servicio.
"""

import logging

from flask import Blueprint, current_app, jsonify, request

from app.services.calculator import execute_operation
from app.utils.formatters import format_number
from app.utils.validators import validate_operation, validate_values

logger = logging.getLogger(__name__)

calculator_bp = Blueprint("calculator", __name__)


@calculator_bp.route("/calculate", methods=["POST"])
def calculate():
    """
    Endpoint principal de cálculo.

    Body JSON esperado:
    {
        "operation": "add" | "subtract" | ... | "convert" | "expression",
        "values": [número, ...],
        "from_unit": "km",      # solo para 'convert'
        "to_unit": "m",         # solo para 'convert'
        "expression": "2+2"     # solo para 'expression'
    }

    Returns:
        200: { "result": <número> }
        400: { "error": "<mensaje>" }
        500: { "error": "<mensaje>" }
    """
    payload = request.get_json(silent=True)

    if not payload:
        return jsonify({"error": "El body debe ser JSON válido."}), 400

    try:
        # 1. Validar campos base del payload
        operation = validate_operation(payload.get("operation"))

        # Las operaciones que no necesitan 'values' numéricos (expression)
        # o que tienen requisitos distintos se validan dentro del handler.
        # Las que sí necesitan values, los validamos aquí con min_count correcto.
        _TWO_VALUE_OPS = {"subtract", "multiply", "divide", "power", "percentage"}
        _ONE_VALUE_OPS = {"sqrt", "log", "factorial", "sin", "cos", "tan", "convert"}

        if operation in _TWO_VALUE_OPS:
            payload["values"] = validate_values(payload.get("values", []), min_count=2)
        elif operation in _ONE_VALUE_OPS:
            payload["values"] = validate_values(payload.get("values", []), min_count=1)
        elif operation == "add":
            payload["values"] = validate_values(payload.get("values", []), min_count=2)
        # 'expression' no requiere 'values'

        # 2. Ejecutar la operación en el servicio
        raw_result = execute_operation(payload)

        # 3. Formatear el resultado
        precision = current_app.config.get("RESULT_PRECISION", 10)
        result = format_number(raw_result, precision=precision)

        logger.info("Operación '%s' → resultado: %s", operation, result)
        return jsonify({"result": result}), 200

    except (ValueError, ZeroDivisionError) as exc:
        logger.warning("Error de validación/cálculo: %s", exc)
        return jsonify({"error": str(exc)}), 400

    except Exception as exc:
        logger.error("Error inesperado en /calculate: %s", exc, exc_info=True)
        return jsonify({"error": "Error interno del servidor."}), 500
