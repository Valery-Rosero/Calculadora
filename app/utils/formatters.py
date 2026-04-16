from typing import Union

def format_number(value: Union[int, float], precision: int = 10) -> Union[int, float]:

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
