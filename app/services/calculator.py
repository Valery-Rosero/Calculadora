import logging
import math
from typing import Any, Callable

from flask import current_app

from app.services.converter import convert_units
from app.utils.validators import validate_expression

logger = logging.getLogger(__name__)

OperationHandler = Callable[[dict], Any]

_OPERATION_REGISTRY: dict[str, OperationHandler] = {}


def register(name: str) -> Callable:

    def decorator(fn: OperationHandler) -> OperationHandler:
        _OPERATION_REGISTRY[name] = fn
        return fn
    return decorator


def execute_operation(payload: dict) -> Any:

    operation = payload.get("operation", "")
    handler = _OPERATION_REGISTRY.get(operation)

    if handler is None:
        raise ValueError(f"Operación no reconocida: '{operation}'.")

    logger.debug("Ejecutando operación: %s | payload: %s", operation, payload)
    return handler(payload)


@register("add")
def _handle_add(payload: dict) -> float:
    values = payload["values"]
    return sum(values)


@register("subtract")
def _handle_subtract(payload: dict) -> float:
    values = payload["values"]
    return values[0] - values[1]


@register("multiply")
def _handle_multiply(payload: dict) -> float:
    values = payload["values"]
    return values[0] * values[1]


@register("divide")
def _handle_divide(payload: dict) -> float:
    values = payload["values"]
    if values[1] == 0:
        raise ZeroDivisionError("No se puede dividir entre cero.")
    return values[0] / values[1]


@register("power")
def _handle_power(payload: dict) -> float:
    values = payload["values"]
    return math.pow(values[0], values[1])


@register("sqrt")
def _handle_sqrt(payload: dict) -> float:
    values = payload["values"]
    if values[0] < 0:
        raise ValueError("No existe raíz cuadrada de un número negativo.")
    return math.sqrt(values[0])


@register("percentage")
def _handle_percentage(payload: dict) -> float:
    values = payload["values"]
    return (values[0] * values[1]) / 100


@register("log")
def _handle_log(payload: dict) -> float:
    values = payload["values"]
    if values[0] <= 0:
        raise ValueError("El logaritmo requiere un número positivo.")
    return math.log10(values[0])


@register("factorial")
def _handle_factorial(payload: dict) -> int:
    values = payload["values"]
    n = int(values[0])
    max_n = current_app.config.get("MAX_FACTORIAL_INPUT", 170)
    if n < 0:
        raise ValueError("El factorial no está definido para números negativos.")
    if n > max_n:
        raise ValueError(f"Número demasiado grande (máximo: {max_n}).")
    return math.factorial(n)


@register("sin")
def _handle_sin(payload: dict) -> float:
    return math.sin(math.radians(payload["values"][0]))


@register("cos")
def _handle_cos(payload: dict) -> float:
    return math.cos(math.radians(payload["values"][0]))


@register("tan")
def _handle_tan(payload: dict) -> float:
    return math.tan(math.radians(payload["values"][0]))


@register("convert")
def _handle_convert(payload: dict) -> float:
    return convert_units(
        value=payload["values"][0],
        from_unit=payload.get("from_unit", ""),
        to_unit=payload.get("to_unit", ""),
    )


@register("expression")
def _handle_expression(payload: dict) -> Any:
    max_len = current_app.config.get("MAX_EXPRESSION_LENGTH", 200)
    expr = validate_expression(payload.get("expression", ""), max_length=max_len)
    return _safe_eval(expr)



_SAFE_MATH_CONTEXT: dict[str, Any] = {
    "sqrt": math.sqrt,
    "pow": math.pow,
    "log": math.log,
    "log10": math.log10,
    "log2": math.log2,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "pi": math.pi,
    "e": math.e,
    "abs": abs,
    "round": round,
    "floor": math.floor,
    "ceil": math.ceil,
    "factorial": math.factorial,
}


def _safe_eval(expression: str) -> Any:

    try:
        return eval(expression, {"__builtins__": {}}, _SAFE_MATH_CONTEXT)  # noqa: S307
    except ZeroDivisionError:
        raise ZeroDivisionError("División entre cero en la expresión.")
    except Exception as exc:
        raise ValueError(f"Expresión inválida: {exc}") from exc
