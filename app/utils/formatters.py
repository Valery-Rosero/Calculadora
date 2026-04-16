"""
Formateadores de resultados.
Centralizar el formateo aquí garantiza consistencia en toda la app
y hace que sea fácil cambiar la presentación de números sin tocar
la lógica de negocio.
"""

from typing import Union


def format_number(value: Union[int, float], precision: int = 10) -> Union[int, float]:
    """
    Formatea un número para presentarlo de forma limpia:
    - Si es entero (o float sin parte decimal), retorna int.
    - Si tiene decimales, los redondea a 'precision' dígitos
      y elimina ceros finales innecesarios.

    Args:
        value:     Número a formatear.
        precision: Máximo de decimales significativos.

    Returns:
        int si el valor es entero, float si tiene decimales.

    Examples:
        >>> format_number(4.0)
        4
        >>> format_number(3.14159265358979)
        3.1415926536
        >>> format_number(0.10000000000)
        0.1
    """
    if not isinstance(value, (int, float)):
        return value

    # Números enteros disfrazados de float (e.g. 4.0 → 4)
    if isinstance(value, float) and value == int(value) and abs(value) < 1e15:
        return int(value)

    # Redondear y limpiar ceros finales
    rounded = round(value, precision)
    # Usamos la representación de string para eliminar ceros finales de forma segura
    formatted_str = f"{rounded:.{precision}f}".rstrip("0").rstrip(".")

    try:
        result = float(formatted_str)
        # Segunda pasada: si al hacer float quedó entero, simplificar
        if result == int(result) and abs(result) < 1e15:
            return int(result)
        return result
    except ValueError:
        # Si algo falla en la conversión, devolver el valor redondeado
        return rounded
