"""
Last Adventurer - Backend API
Flask server para el frontend
"""
import sys
import os
from pathlib import Path

# Añadir src al path para imports
backend_dir = Path(__file__).parent
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))

from flask import Flask, jsonify, request
from flask_cors import CORS
import json

from systems.save_manager import SaveManager
from game_manager import crear_nuevo_personaje, calcular_recompensa_exploracion
from models.personaje import Personaje
from api.exploracion import exploracion_bp
from api.combate import combate_bp
from api.mapa import mapa_bp

# Crear la aplicación Flask
app = Flask(__name__)

# Configurar CORS para permitir requests del frontend
CORS(app, resources={
    r"/api/.*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Registrar blueprints
app.register_blueprint(exploracion_bp, url_prefix="/api/exploracion")
app.register_blueprint(combate_bp, url_prefix="/api/combate")
app.register_blueprint(mapa_bp, url_prefix="/api/mapa")

# Instancia global del SaveManager
save_manager = SaveManager()


# ============== HELPERS ==============

def api_response(success, message, data=None, status_code=200):
    """Respuesta estándar de la API"""
    response = {
        "success": success,
        "message": message
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code


def api_error(message, status_code=400):
    """Respuesta de error"""
    return jsonify({"success": False, "message": message}), status_code


# ============== ENDPOINTS ==============

@app.route("/")
def root():
    """Endpoint raíz"""
    return jsonify({"message": "Last Adventurer API", "version": "1.0.0"})


@app.route("/api/slots", methods=["GET"])
def obtener_slots():
    """Obtiene información de todos los slots de guardado"""
    slots = []
    for slot_num in range(1, SaveManager.NUM_SLOTS + 1):
        info = save_manager.obtener_info_slot(slot_num)
        slots.append({
            "numero": slot_num,
            "ocupado": info is not None,
            "info": info
        })
    return jsonify({"slots": slots})


@app.route("/api/slots/<int:slot_num>", methods=["GET"])
def obtener_slot(slot_num):
    """Obtiene información de un slot específico"""
    if not 1 <= slot_num <= SaveManager.NUM_SLOTS:
        return api_error(f"Slot inválido. Debe ser entre 1 y {SaveManager.NUM_SLOTS}")
    
    info = save_manager.obtener_info_slot(slot_num)
    return jsonify({
        "numero": slot_num,
        "ocupado": info is not None,
        "info": info
    })


@app.route("/api/partida/nueva", methods=["POST"])
def nueva_partida():
    """Crea una nueva partida"""
    data = request.get_json()
    
    if not data:
        return api_error("No se enviaron datos")
    
    nombre = data.get("nombre", "")
    genero = data.get("genero", "no_especificar").lower()
    dificultad = data.get("dificultad", "normal").lower()
    
    # Validar nombre
    if len(nombre) < 3:
        return api_error("El nombre debe tener al menos 3 caracteres")
    
    # Validar género
    generos_validos = ["masculino", "femenino", "no_especificar"]
    if genero not in generos_validos:
        return api_error(f"Género inválido. Debe ser uno de: {generos_validos}")
    
    # Validar dificultad
    dificultades_validas = ["facil", "normal", "dificil"]
    if dificultad not in dificultades_validas:
        return api_error(f"Dificultad inválida. Debe ser una de: {dificultades_validas}")
    
    # Buscar slot libre
    slot_libre = None
    for slot_num in range(1, SaveManager.NUM_SLOTS + 1):
        if not save_manager.slot_existe(slot_num):
            slot_libre = slot_num
            break
    
    if slot_libre is None:
        return api_error("Todos los slots están ocupados")
    
    # Crear personaje mediante el game_manager desacoplado
    personaje, mensaje_creacion = crear_nuevo_personaje(
        nombre=nombre,
        genero=genero,
        dificultad=dificultad
    )
    
    if not personaje:
        return api_error(mensaje_creacion)
    
    # Obtener el diccionario completo para guardar
    datos_partida = save_manager.crear_save_vacio(
        nombre=nombre,
        genero=genero,
        dificultad=dificultad
    )
    
    # Sincronizar stats y habilidades iniciales del modelo Personaje
    datos_partida["personaje"] = personaje.to_dict()
    
    # Guardar
    exito, mensaje = save_manager.guardar(slot_libre, datos_partida)
    
    if not exito:
        return api_error(mensaje, 500)
    
    return api_response(True, mensaje, {"slot": slot_libre, "datos": datos_partida})


@app.route("/api/partida/<int:slot_num>", methods=["GET"])
def cargar_partida(slot_num):
    """Carga una partida desde un slot"""
    if not 1 <= slot_num <= SaveManager.NUM_SLOTS:
        return api_error(f"Slot inválido. Debe ser entre 1 y {SaveManager.NUM_SLOTS}")
    
    datos, mensaje = save_manager.cargar(slot_num)
    
    if not datos:
        return api_error(mensaje, 404)
    
    return api_response(True, mensaje, datos)


@app.route("/api/partida/<int:slot_num>", methods=["PUT"])
def guardar_partida(slot_num):
    """Guarda una partida en un slot"""
    if not 1 <= slot_num <= SaveManager.NUM_SLOTS:
        return api_error(f"Slot inválido. Debe ser entre 1 y {SaveManager.NUM_SLOTS}")
    
    data = request.get_json()
    
    if not data or "datos" not in data:
        return api_error("No se enviaron datos para guardar")
    
    exito, mensaje = save_manager.guardar(slot_num, data["datos"])
    
    if not exito:
        return api_error(mensaje, 500)
    
    return api_response(True, mensaje)


@app.route("/api/partida/<int:slot_num>", methods=["DELETE"])
def eliminar_partida(slot_num):
    """Elimina una partida de un slot"""
    if not 1 <= slot_num <= SaveManager.NUM_SLOTS:
        return api_error(f"Slot inválido. Debe ser entre 1 y {SaveManager.NUM_SLOTS}")
    
    exito, mensaje = save_manager.eliminar(slot_num)
    
    if not exito:
        return api_error(mensaje, 404)
    
    return api_response(True, mensaje)


@app.route("/api/personaje/<int:slot_num>", methods=["GET"])
def obtener_personaje(slot_num):
    """Obtiene los datos del personaje de una partida"""
    if not 1 <= slot_num <= SaveManager.NUM_SLOTS:
        return api_error(f"Slot inválido. Debe ser entre 1 y {SaveManager.NUM_SLOTS}")
    
    datos, _ = save_manager.cargar(slot_num)
    
    if not datos:
        return api_error("Partida no encontrada", 404)
    
    return jsonify({
        "success": True,
        "data": datos.get("personaje", {})
    })


# ============== ENDPOINTS DE DATOS ==============

# ============== ENDPOINTS DE JUEGO ==============

@app.route("/api/personaje/stats/mejorar", methods=["POST"])
def mejorar_stat():
    """Mejora un stat del personaje usando puntos disponibles"""
    data = request.get_json()
    if not data or "slot" not in data or "stat" not in data:
        return api_error("Faltan datos (slot, stat)")
    
    slot_num = data["slot"]
    stat_nombre = data["stat"]
    cantidad = data.get("cantidad", 1)
    
    datos, _ = save_manager.cargar(slot_num)
    if not datos:
        return api_error("Partida no encontrada", 404)
    
    personaje = Personaje.from_dict(datos["personaje"])
    
    # Mapeo de stats a métodos
    metodos = {
        "hp": personaje.stats.asignar_hp,
        "ataque": personaje.stats.asignar_atk,
        "defensa": personaje.stats.asignar_def,
        "velocidad": personaje.stats.asignar_velocidad,
        "critico": personaje.stats.asignar_critico,
        "evasion": personaje.stats.asignar_evasion,
        "mana": personaje.stats.asignar_mana,
        "stamina": personaje.stats.asignar_stamina
    }
    
    if stat_nombre not in metodos:
        return api_error(f"Stat inválido: {stat_nombre}")
    
    exito, mensaje = metodos[stat_nombre](cantidad)
    
    if exito:
        # Actualizar el dict de datos y guardar
        datos["personaje"] = personaje.to_dict()
        save_manager.guardar(slot_num, datos)
        return api_response(True, mensaje, datos["personaje"])
    else:
        return api_error(mensaje)

@app.route("/api/juego/explorar", methods=["POST"])
def explorar():
    """Simula una acción de exploración"""
    data = request.get_json()
    if not data or "slot" not in data:
        return api_error("Falta el slot")
    
    slot_num = data["slot"]
    datos, _ = save_manager.cargar(slot_num)
    if not datos:
        return api_error("Partida no encontrada", 404)
    
    personaje = Personaje.from_dict(datos["personaje"])
    
    # Calcular recompensas
    oro, exp = calcular_recompensa_exploracion(personaje.get_nivel())
    
    # Aplicar recompensas
    datos["inventario"]["oro"] += oro
    exito_exp, msg_exp = personaje.ganar_experiencia(exp)
    
    # Actualizar datos del personaje (stats/nivel)
    datos["personaje"] = personaje.to_dict()
    
    # Guardar progreso
    save_manager.guardar(slot_num, datos)
    
    resultado = {
        "mensaje": f"Has explorado la zona y encontrado {oro} oro. {msg_exp}",
        "recompensas": {"oro": oro, "exp": exp},
        "personaje": datos["personaje"],
        "inventario": datos["inventario"]
    }
    
    return api_response(True, "Exploración completada", resultado)



# ============== INICIO DEL SERVIDOR ==============

if __name__ == "__main__":
    print("Last Adventurer API - Flask")
    print("Servidor corriendo en http://localhost:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
