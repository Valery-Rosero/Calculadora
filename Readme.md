# 🧮 CalcPro — Calculadora Inteligente Python

Calculadora con interfaz web construida con **Flask** (Python) + HTML/CSS/JS.

---

## 📁 Estructura

```
calculator/
├── app.py              # Backend Flask (API REST)
├── requirements.txt    # Dependencias
└── static/
    └── index.html      # Interfaz (frontend)
```

---

## 🚀 Cómo ejecutar

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```
### importanteeeeeee ####
### 2. Correr el servidor
```bash
python app.py
```

### 3. Abrir en el navegador
```
http://localhost:5000
```

---

## ⚙️ Funcionalidades

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

---

## 🌐 Endpoints de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/calculate` | Operación matemática |

### Ejemplo de petición
```json
POST /calculate
{
  "operation": "sqrt",
  "values": [144]
}
```
```json
// Respuesta
{ "result": 12 }
```

### Operaciones disponibles
`add`, `subtract`, `multiply`, `divide`, `power`, `sqrt`, `percentage`, `log`, `factorial`, `sin`, `cos`, `tan`, `abs`, `convert`, `expression`