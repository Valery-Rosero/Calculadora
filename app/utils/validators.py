"""
Validadores de entrada.
Cada función valida una parte del payload del request
y lanza ValueError con mensajes claros si algo falla.
Separar validaciones aquí evita contaminar la lógica de negocio.
"""

from typing import Any


def validate_values(values: Any, min_count: int = 1) -> list:
    """
    Valida que 'values' sea una lista de números con suficientes elementos.

    Args:
        values:    El valor recibido del payload JSON.
        min_count: Mínimo de elementos requeridos.

    Raises:
        ValueError: Si la estructura o los tipos no son válidos.
    """
    if not isinstance(values, list):
        raise ValueError("'values' debe ser una lista.")

    if len(values) < min_count:
        raise ValueError(
            f"Se requieren al menos {min_count} valor(es), "
            f"se recibieron {len(values)}."
        )

    for i, v in enumerate(values):
        if not isinstance(v, (int, float)):
            raise ValueError(
                f"El elemento en posición {i} no es un número válido: '{v}'."
            )

    return values


def validate_operation(operation: Any) -> str:
    """
    Valida que 'operation' sea un string no vacío.

    Raises:
        ValueError: Si el valor no es un string válido.
    """
    if not isinstance(operation, str) or not operation.strip():
        raise ValueError("'operation' debe ser un string no vacío.")
    return operation.strip()


def validate_expression(expression: Any, max_length: int = 200) -> str:
    """
    Valida una expresión matemática libre.

    Args:
        expression: El string de la expresión.
        max_length:  Longitud máxima permitida.

    Raises:
        ValueError: Si la expresión no es segura o está mal formada.
    """
    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("'expression' debe ser un string no vacío.")

    if len(expression) > max_length:
        raise ValueError(
            f"La expresión excede el límite de {max_length} caracteres."
        )

    # Caracteres permitidos: dígitos, operadores, paréntesis,
    # punto decimal, espacios y letras para funciones nombradas.
    allowed_chars = set("0123456789+-*/().^ ,_abcdefghijklmnopqrstuvwxyz")
    invalid = {c for c in expression.lower() if c not in allowed_chars}
    if invalid:
        raise ValueError(
            f"La expresión contiene caracteres no permitidos: {invalid}"
        )

    return expression.strip()


def validate_units(from_unit: Any, to_unit: Any) -> tuple[str, str]:
    """
    Valida que ambas unidades sean strings no vacíos.

    Raises:
        ValueError: Si alguna unidad es inválida.
    """
    if not isinstance(from_unit, str) or not from_unit.strip():
        raise ValueError("'from_unit' debe ser un string no vacío.")
    if not isinstance(to_unit, str) or not to_unit.strip():
        raise ValueError("'to_unit' debe ser un string no vacío.")
    return from_unit.strip(), to_unit.strip()
