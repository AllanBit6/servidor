from flask import Flask, jsonify, request
import gunicorn
from sqlite3 import *
import os

def connect_db():
    conn = connect('estudiantes.db')
    cr = conn.cursor()
    cr.execute('''
        CREATE TABLE IF NOT EXISTS estudiantes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    return True

def getEstudiantesDB():
    conn = connect('estudiantes.db')
    conn.row_factory = Row
    cr = conn.cursor()
    cr.execute('SELECT * FROM estudiantes')
    ests = cr.fetchall()

    # Convertir cada fila a dict
    estudiantes = [dict(est) for est in ests]
    conn.close()
    return estudiantes

def getEstudiantesByIdDB(estudiante_id):
    conn = connect('estudiantes.db')
    conn.row_factory = Row
    cr = conn.cursor()
    cr.execute('SELECT * FROM estudiantes WHERE id = ?', (estudiante_id,))
    ests = cr.fetchall()
    estudiante = [dict(est) for est in ests]
    conn.close()
    return estudiante

def createEstudianteDB(nombre, edad):
    conn = connect('estudiantes.db')
    cr = conn.cursor()

    try:
        cr.execute('INSERT INTO estudiantes (nombre, edad) VALUES (?, ?)', (nombre, edad))
        conn.commit()
        conn.close()
        return True
    except:
        return False


app = Flask(__name__)

@app.route('/')
def root():
    connect_db()
    return "Home"

#Obtener todos los estudiantes
@app.route('/estudiante', methods=['GET'])
def get_estudiantes():
    estudiantes = getEstudiantesDB()
    return jsonify(estudiantes), 200

#Obtener solo un estudiante por ID
@app.route('/estudiante/<estudiante_id>', methods=['GET'])
def get_estudiante(estudiante_id):
    estudiante = getEstudiantesByIdDB(estudiante_id)
    
   
    if estudiante:
        return jsonify(estudiante), 200
    else:
        return jsonify({"error": "Estudiante no encontrado"}), 404

#Metodo para crear un estudiante
@app.route('/estudiante', methods=['POST'])
def create_estudiante():
    data = request.get_json()

    if createEstudianteDB(data['nombre'], data['edad']):
        return jsonify(data), 201
    else:
        return jsonify({"error": "Error al crear el estudiante"}), 500
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

