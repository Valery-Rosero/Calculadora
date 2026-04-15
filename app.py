from flask import Flask, request, jsonify, send_from_directory
import math
import os

app = Flask(__name__, static_folder='static')

def safe_eval_expression(expr):
    """Evalúa expresiones matemáticas de forma segura."""
    allowed_names = {
        'sqrt': math.sqrt, 'pow': math.pow, 'log': math.log,
        'log10': math.log10, 'log2': math.log2, 'sin': math.sin,
        'cos': math.cos, 'tan': math.tan, 'pi': math.pi,
        'e': math.e, 'abs': abs, 'round': round,
        'floor': math.floor, 'ceil': math.ceil,
        'factorial': math.factorial,
    }
    try:
        result = eval(expr, {"__builtins__": {}}, allowed_names)
        return result
    except Exception as e:
        raise ValueError(f"Expresión inválida: {e}")

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    operation = data.get('operation')
    values = data.get('values', [])
    
    try:
        result = None

        # Operaciones básicas
        if operation == 'add':
            result = sum(values)
        elif operation == 'subtract':
            result = values[0] - values[1]
        elif operation == 'multiply':
            result = values[0] * values[1]
        elif operation == 'divide':
            if values[1] == 0:
                return jsonify({'error': 'No se puede dividir entre cero'}), 400
            result = values[0] / values[1]

        # Operaciones avanzadas
        elif operation == 'power':
            result = math.pow(values[0], values[1])
        elif operation == 'sqrt':
            if values[0] < 0:
                return jsonify({'error': 'No existe raíz de número negativo'}), 400
            result = math.sqrt(values[0])
        elif operation == 'percentage':
            result = (values[0] * values[1]) / 100
        elif operation == 'log':
            if values[0] <= 0:
                return jsonify({'error': 'El logaritmo requiere número positivo'}), 400
            result = math.log10(values[0])
        elif operation == 'factorial':
            n = int(values[0])
            if n < 0:
                return jsonify({'error': 'Factorial no definido para negativos'}), 400
            if n > 170:
                return jsonify({'error': 'Número demasiado grande para factorial'}), 400
            result = math.factorial(n)
        elif operation == 'sin':
            result = math.sin(math.radians(values[0]))
        elif operation == 'cos':
            result = math.cos(math.radians(values[0]))
        elif operation == 'tan':
            result = math.tan(math.radians(values[0]))

        # Conversión de unidades
        elif operation == 'convert':
            value = values[0]
            from_unit = data.get('from_unit')
            to_unit = data.get('to_unit')
            result = convert_units(value, from_unit, to_unit)

        # Expresión libre
        elif operation == 'expression':
            expr = data.get('expression', '')
            result = safe_eval_expression(expr)

        else:
            return jsonify({'error': 'Operación no reconocida'}), 400

        # Formateo del resultado
        if isinstance(result, float):
            if result == int(result) and abs(result) < 1e15:
                result = int(result)
            else:
                result = round(result, 10)
                # Eliminar ceros finales
                result_str = f"{result:.10f}".rstrip('0').rstrip('.')
                try:
                    result = float(result_str)
                except:
                    pass

        return jsonify({'result': result})

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500


def convert_units(value, from_unit, to_unit):
    """Conversiones de unidades."""
    conversions = {
        # Longitud (base: metros)
        'km': 1000, 'm': 1, 'cm': 0.01, 'mm': 0.001,
        'mi': 1609.344, 'ft': 0.3048, 'in': 0.0254, 'yd': 0.9144,

        # Peso (base: kg)
        'kg': 1, 'g': 0.001, 'mg': 0.000001,
        'lb': 0.453592, 'oz': 0.0283495, 't': 1000,

        # Temperatura (especial)
        'C': 'temp', 'F': 'temp', 'K': 'temp',

        # Velocidad (base: m/s)
        'ms': 1, 'kmh': 0.277778, 'mph': 0.44704, 'knot': 0.514444,

        # Área (base: m²)
        'm2': 1, 'km2': 1e6, 'cm2': 0.0001, 'ft2': 0.092903, 'ac': 4046.86,

        # Volumen (base: litros)
        'l': 1, 'ml': 0.001, 'm3': 1000, 'gal': 3.78541, 'fl_oz': 0.0295735,
    }

    # Temperatura
    if from_unit in ('C', 'F', 'K') or to_unit in ('C', 'F', 'K'):
        return convert_temperature(value, from_unit, to_unit)

    if from_unit not in conversions or to_unit not in conversions:
        raise ValueError(f'Unidad no reconocida: {from_unit} o {to_unit}')

    # Convertir a base y luego al destino
    base_value = value * conversions[from_unit]
    return base_value / conversions[to_unit]


def convert_temperature(value, from_unit, to_unit):
    """Conversión de temperatura."""
    # A Celsius primero
    if from_unit == 'C':
        celsius = value
    elif from_unit == 'F':
        celsius = (value - 32) * 5/9
    elif from_unit == 'K':
        celsius = value - 273.15
    else:
        raise ValueError('Unidad de temperatura inválida')

    # De Celsius al destino
    if to_unit == 'C':
        return celsius
    elif to_unit == 'F':
        return celsius * 9/5 + 32
    elif to_unit == 'K':
        return celsius + 273.15
    else:
        raise ValueError('Unidad de temperatura inválida')


if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    app.run(debug=True, port=5000)