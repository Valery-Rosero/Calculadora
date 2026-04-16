# 🧮 CalcPro — Calculadora Inteligente Python

Calculadora con interfaz web construida con **Flask** (Python) + HTML/CSS/JS.

---

## 📁 Estructura

```
config.py
run.py
requirements.txt
app/
    __init__.py
    routes/
        calculator.py
        static_pages.py
    services/
        calculator.py
        converter.py
    utils/
        formatters.py
        validators.py
static/
    index.html
```

---

##  Cómo ejecutar

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Correr el servidor
```bash
python run.py
```

### 3. Abrir en el navegador
```
http://localhost:5000
```

---

##  Funcionalidades

### Básica
- Suma, resta, multiplicación, división
- Soporte para decimales, cambio de signo
- Porcentaje rápido
- Soporte de teclado (↑ útil para desktops)

### Avanzada
- Raíz cuadrada (`√x`)
- Cuadrado (`x²`) y potencia (`xʸ`)
- Logaritmo base 10
- Factorial (`n!`)
- Inverso (`1/x`)
- Funciones trigonométricas: sin, cos, tan (en grados)
- Valor absoluto
- Constantes: π y e

### Conversión de unidades
| Categoría     | Unidades disponibles |
|---------------|----------------------|
| Longitud      | m, km, cm, mm, mi, ft, in, yd |
| Peso / Masa   | kg, g, mg, lb, oz, t |
| Temperatura   | °C, °F, K |
| Velocidad     | m/s, km/h, mph, knot |
| Área          | m², km², cm², ft², ac |
| Volumen       | L, mL, m³, gal, fl oz |

### Historial
- Guarda las últimas 50 operaciones
- Clic en cualquier resultado para reutilizarlo

## Participacion ##

  <Johan Delgado>
    API REST separada con Flask y endpoint principal en `/api/calculate`
    Arquitectura modular con carpetas diferenciadas para rutas, servicios y utilidades
    Configuración centralizada en `config.py` y arranque por `run.py`
    se edito la arquitectura monolítica para facilitar mantenimiento y escalabilidad :p

  <Juan Manuel Matabanchoy>

    Estructuracion frontend y estilos

  <Valery Rosero>
    
    Creacion repositorio  logica en javascript 
