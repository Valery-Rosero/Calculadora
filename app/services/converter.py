
import logging

logger = logging.getLogger(__name__)

# Base: metros
LENGTH_UNITS: dict[str, float] = {
    "km": 1000,
    "m": 1,
    "cm": 0.01,
    "mm": 0.001,
    "mi": 1609.344,
    "ft": 0.3048,
    "in": 0.0254,
    "yd": 0.9144,
}

# Base: kilogramos
WEIGHT_UNITS: dict[str, float] = {
    "kg": 1,
    "g": 0.001,
    "mg": 0.000001,
    "lb": 0.453592,
    "oz": 0.0283495,
    "t": 1000,
}

# Base: metros por segundo
SPEED_UNITS: dict[str, float] = {
    "ms": 1,
    "kmh": 0.277778,
    "mph": 0.44704,
    "knot": 0.514444,
}

# Base: metros cuadrados
AREA_UNITS: dict[str, float] = {
    "m2": 1,
    "km2": 1e6,
    "cm2": 0.0001,
    "ft2": 0.092903,
    "ac": 4046.86,
}

# Base: litros
VOLUME_UNITS: dict[str, float] = {
    "l": 1,
    "ml": 0.001,
    "m3": 1000,
    "gal": 3.78541,
    "fl_oz": 0.0295735,
}

TEMPERATURE_UNITS = {"C", "F", "K"}

# Índice: unidad → dimensión a la que pertenece
_UNIT_DIMENSION_INDEX: dict[str, dict] = {}

for _table in [LENGTH_UNITS, WEIGHT_UNITS, SPEED_UNITS, AREA_UNITS, VOLUME_UNITS]:
    for _unit in _table:
        _UNIT_DIMENSION_INDEX[_unit] = _table


def convert_units(value: float, from_unit: str, to_unit: str) -> float:

    # Temperatura tiene lógica especial (no es multiplicativa)
    if from_unit in TEMPERATURE_UNITS or to_unit in TEMPERATURE_UNITS:
        return _convert_temperature(value, from_unit, to_unit)

    if from_unit not in _UNIT_DIMENSION_INDEX:
        raise ValueError(f"Unidad no reconocida: '{from_unit}'.")

    if to_unit not in _UNIT_DIMENSION_INDEX:
        raise ValueError(f"Unidad no reconocida: '{to_unit}'.")

    from_table = _UNIT_DIMENSION_INDEX[from_unit]
    to_table = _UNIT_DIMENSION_INDEX[to_unit]

    # Detectar conversión entre dimensiones distintas (e.g. km → kg)
    if from_table is not to_table:
        raise ValueError(
            f"No se puede convertir '{from_unit}' a '{to_unit}': "
            "son de distinto tipo físico."
        )

    logger.debug("Convirtiendo %.6f %s → %s", value, from_unit, to_unit)

    base_value = value * from_table[from_unit]
    return base_value / to_table[to_unit]


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:

    if from_unit not in TEMPERATURE_UNITS:
        raise ValueError(f"Unidad de temperatura inválida: '{from_unit}'.")
    if to_unit not in TEMPERATURE_UNITS:
        raise ValueError(f"Unidad de temperatura inválida: '{to_unit}'.")

    # Paso 1: convertir a Celsius
    to_celsius = {
        "C": lambda v: v,
        "F": lambda v: (v - 32) * 5 / 9,
        "K": lambda v: v - 273.15,
    }
    celsius = to_celsius[from_unit](value)

    # Paso 2: convertir de Celsius al destino
    from_celsius = {
        "C": lambda c: c,
        "F": lambda c: c * 9 / 5 + 32,
        "K": lambda c: c + 273.15,
    }
    return from_celsius[to_unit](celsius)
