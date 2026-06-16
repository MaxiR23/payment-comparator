# Payment Comparator

Comparador de cupones de pago (Áulica) contra planilla de control mensual.
Detecta diferencias, alumnos faltantes y genera un informe en Excel.

Tiene dos modos: **web** (Flask) y **CLI**.

## Estructura

```
payment-comparator/
├── app.py                  # entrada Flask (web)
├── main.py                 # entrada CLI
├── compare.py              # orquesta el flujo (leer → comparar → escribir)
├── config/
│   └── settings.py         # mes, año, tolerancia — actualizar cada ciclo
├── src/
│   ├── reader.py           # lectura y normalización de Excel
│   ├── comparator.py       # lógica de comparación
│   └── writer.py           # generación del informe Excel
├── templates/
│   └── index.html          # interfaz web
├── static/
│   ├── css/style.css
│   └── js/                 # main.js, api.js, files.js, state.js, ui.js
├── tests/
│   └── test_comparator.py
├── data/                   # Excel de entrada (CLI)
├── uploads/                # archivos temporales (web, se limpian solos)
└── output/                 # informes generados
```

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Modo web

```bash
python app.py
# → http://127.0.0.1:8080
```

En producción con gunicorn:

```bash
gunicorn -w 2 -b 127.0.0.1:5000 app:app
```

Ver `deploy.md` para la configuración completa con nginx + systemd + HTTPS.

## Modo CLI

```bash
# auto-detecta archivos en data/ por nombre (AULICA / CONTROL)
python main.py

# o con rutas explícitas
python main.py ruta/aulica.xlsx ruta/control.xlsx
```

El informe se genera en `output/` con timestamp en el nombre.

## Cambio de mes

Editá `config/settings.py`:

```python
MONTH = "MAYO"
YEAR  = 2026
```

El nombre de hoja y la columna de cuota se actualizan solos.

## Tests

```bash
pytest tests/test_comparator.py -v
```

## Salida

El informe Excel tiene dos solapas:

- **Diferencias** — alumnos donde la suma de cupones Áulica ≠ total del Control
- **Solo en Control** — alumnos presentes en Control sin cupones en Áulica