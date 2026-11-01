import os
import psycopg2
from flask import Flask, render_template_string

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        connect_timeout=5,
    )


HOME = """
<!doctype html>
<html lang="es">
<head><meta charset="utf-8"><title>Plataforma de sensores</title></head>
<body>
  <h1>Plataforma de sensores</h1>
  <p>Aplicación de consulta de lecturas simuladas.</p>
  <p><a href="/lecturas">Ver lecturas</a></p>
</body>
</html>
"""

LECTURAS = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Lecturas</title>
  <style>
    table { border-collapse: collapse; }
    th, td { border: 1px solid #999; padding: 6px 12px; }
    th { background: #eee; }
  </style>
</head>
<body>
  <h1>Lecturas</h1>
  <p><a href="/">Volver al inicio</a></p>
  {% if error %}
    <p><strong>Error:</strong> {{ error }}</p>
  {% elif not filas %}
    <p>No hay lecturas registradas todavía.</p>
  {% else %}
    <table>
      <tr>
        <th>ID</th><th>Dispositivo</th><th>Tipo</th>
        <th>Valor</th><th>Origen</th><th>Fecha</th>
      </tr>
      {% for f in filas %}
      <tr>
        <td>{{ f[0] }}</td><td>{{ f[1] }}</td><td>{{ f[2] }}</td>
        <td>{{ f[3] }}</td><td>{{ f[4] }}</td><td>{{ f[5] }}</td>
      </tr>
      {% endfor %}
    </table>
  {% endif %}
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HOME)


@app.route("/lecturas")
def lecturas():
    try:
        conn = get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, dispositivo, tipo, valor, origen, creado_en "
                    "FROM lecturas ORDER BY id DESC"
                )
                filas = cur.fetchall()
        finally:
            conn.close()
        return render_template_string(LECTURAS, filas=filas, error=None)
    except Exception:
        return render_template_string(
            LECTURAS, filas=[], error="No se pudo conectar a la base de datos."
        ), 500