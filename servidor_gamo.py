from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# URL ACTUALIZADA CON TU NUEVA CLAVE
DB_URL = "postgresql://luis:DUQbdff_9SrVDgBNj2mziw@hearty-sphinx-14305.jxf.gcp-us-east1.cockroachlabs.cloud:26257/loligg?sslmode=verify-full"

@app.route('/guardar', methods=['POST'])
def guardar():
    datos = request.json
    conn = None
    try:
        # Intentar conectar con la nueva clave
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Insertar datos en la tabla 'partida'
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
        # Si sale error de "too many attempts", hay que esperar 2 min
        return jsonify({"status": "error", "detalle": str(e)}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    print("---------------------------------------------")
    print("   SERVIDOR GAMOGAMING - ESTADO: ACTIVO      ")
    print("   CON NUEVA CLAVE CONFIGURADA               ")
    print("---------------------------------------------")
    app.run(host='0.0.0.0', port=5000)


    if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)