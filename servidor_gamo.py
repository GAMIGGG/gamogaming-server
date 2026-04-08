from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# URL ACTUALIZADA CON TU NUEVA CLAVE
# Cambiamos sslmode a 'require' para que no pida el archivo root.crt
# Cambiamos sslmode a 'verify-full' y añadimos sslrootcert=system
# Cambiamos sslmode a 'no-verify' para que CockroachDB no se ponga estricto
# Esta versión apaga por completo la exigencia del certificado SSL
# 'require' activa la encriptación necesaria sin pedir el archivo físico
DB_URL = "postgresql://luis:DUQbdff_9SrVDgBNj2mziw@hearty-sphinx-14305.jxf.gcp-us-east1.cockroachlabs.cloud:26257/loligg?sslmode=require"

@app.route('/guardar', methods=['POST'])
def guardar():
    datos = request.json
    conn = None
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO partida (nombre_jugador, nivel, monedas) VALUES (%s, %s, %s)", 
            (datos['nombre'], datos['nivel'], datos['monedas'])
        )
        
        conn.commit()
        cur.close()
        print(f"-> ¡ÉXITO TOTAL! Guardado progreso de {datos['nombre']}")
        return jsonify({"status": "exito"}), 200

    except Exception as e:
        print(f"-> ERROR DE CONEXIÓN: {e}")
        return jsonify({"status": "error", "detalle": str(e)}), 500
    finally:
        if conn:
            conn.close()

# ESTA ES LA PARTE QUE DABA ERROR (Corregida con espacios)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"--- SERVIDOR GAMOGAMING ACTIVO EN PUERTO {port} ---")
    app.run(host='0.0.0.0', port=port)
