from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import extras
from flask_cors import CORS # Importa la extensión CORS

app = Flask(__name__)
CORS(app) # Inicializa CORS con tu aplicación Flask.
          # Por defecto, esto permite peticiones desde cualquier origen ('*').
          # En producción, querrías restringirlo a tu dominio.

# Configuración de la conexión a la base de datos
DB_HOST = "190.114.255.100" # O la IP/dominio de tu servidor de DB
DB_NAME = "proalto"
DB_USER = "monsalve"
DB_PASS = "m0ns@lv301"
doc_id = "10005"

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    return conn

@app.route('/saldo', methods=['GET'])
def get_saldo():
    documento = request.args.get('documento') # Obtiene el parámetro 'documento' de la URL
    #documento = doc_id

    if not documento:
        return jsonify({"error": "Debe proporcionar un número de documento."}), 400

    conn = None
    cur = None
    try:
        conn = get_db_connection()
        # Usar RealDictCursor para obtener filas como diccionarios
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Asegúrate de que tu vista se llama 'saldos_prestamos_clientes'
        # y que el campo para el documento se llama 'cedula_identidad' (ajusta si es diferente)
        #query = "SELECT * FROM saldos_prestamos_clientes WHERE cedula_identidad = %s"
        query = "SELECT * FROM vista_saldos_prestamos WHERE id_prestamo = %s"
        #query = "SELECT * FROM vista_saldos_prestamos WHERE id_prestamo = '10005'"
        cur.execute(query, (documento,)) 
        
        saldo_data = cur.fetchone() # Asumiendo que un documento solo tiene un saldo de préstamo activo o quieres el primero

        if saldo_data:
            return jsonify(saldo_data), 200
        else:
            return jsonify({"mensaje": "No se encontró un préstamo para el documento proporcionado."}), 404

    except Exception as e:
        print(f"Error al consultar la base de datos: {e}")
        return jsonify({"error": "Error interno del servidor."}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True) # debug=True recarga el servidor automáticamente con cambios y muestra errores