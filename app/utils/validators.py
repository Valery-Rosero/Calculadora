from typing import Any


def validate_values(values: Any, min_count: int = 1) -> list:
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
    
    if not isinstance(operation, str) or not operation.strip():
        raise ValueError("'operation' debe ser un string no vacío.")
    return operation.strip()


def validate_expression(expression: Any, max_length: int = 200) -> str:
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
    if not isinstance(from_unit, str) or not from_unit.strip():
        raise ValueError("'from_unit' debe ser un string no vacío.")
    if not isinstance(to_unit, str) or not to_unit.strip():
        raise ValueError("'to_unit' debe ser un string no vacío.")
    return from_unit.strip(), to_unit.strip()
