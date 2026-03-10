"""
API de Combate para Last Adventurer.
Endpoints para gestionar combates.
"""

from flask import Blueprint, request, jsonify
import json
import os
from systems.combate import CombateManager, EstadoCombate
from models.personaje import Personaje
from systems.save_manager import SaveManager

combate_bp = Blueprint('combate', __name__)

# Instancia global del manager de combate (en producción usar Redis o similar)
combate_activo = None


def api_response(success, message, data=None, status_code=200):
    """Helper para respuestas estándar"""
    response = {"success": success, "message": message}
    if data:
        response["data"] = data
    return jsonify(response), status_code


def cargar_enemigos_data():
    """Carga los datos de enemigos desde JSON"""
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'enemigos.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


@combate_bp.route('/iniciar', methods=['POST'])
def iniciar_combate():
    """Inicia un nuevo combate"""
    global combate_activo
    
    data = request.get_json()
    slot = data.get('slot', 1)
    enemigos_ids = data.get('enemigos', [])
    zona = data.get('zona', 'bosque')
    
    if not enemigos_ids:
        return api_response(False, "No se especificaron enemigos", status_code=400)
    
    # Cargar personaje
    save_manager = SaveManager()
    datos_juego = save_manager.cargar(slot)
    if not datos_juego:
        return api_response(False, "No se encontró la partida", status_code=404)
    
    personaje = Personaje.from_dict(datos_juego['personaje'])
    
    # Cargar datos de enemigos
    enemigos_data = cargar_enemigos_data()
    enemigos_template = []
    
    for eid in enemigos_ids:
        # Buscar en todas las categorías
        for categoria, lista in enemigos_data['enemigos'].items():
            for template in lista:
                if template['id'] == eid:
                    enemigos_template.append(template)
                    break
    
    if not enemigos_template:
        return api_response(False, "No se encontraron los enemigos especificados", status_code=404)
    
    # Crear manager de combate
    combate_activo = CombateManager()
    estado = combate_activo.iniciar_combate(personaje, enemigos_template)
    
    return api_response(True, "Combate iniciado", estado)


@combate_bp.route('/accion', methods=['POST'])
def ejecutar_accion():
    """Ejecuta una acción del jugador en combate"""
    global combate_activo
    
    if not combate_activo:
        return api_response(False, "No hay combate activo", status_code=400)
    
    data = request.get_json()
    actor_id = data.get('actor_id', 'jugador_1')
    accion = data.get('accion')
    objetivo_id = data.get('objetivo_id')
    habilidad_nombre = data.get('habilidad_nombre')
    item_id = data.get('item_id')
    
    if not accion:
        return api_response(False, "No se especificó acción", status_code=400)
    
    resultado = combate_activo.ejecutar_accion(
        actor_id, accion, objetivo_id, habilidad_nombre, item_id
    )
    
    return api_response(True, "Acción ejecutada", resultado)


@combate_bp.route('/resolver-enemigos', methods=['POST'])
def resolver_enemigos():
    """Resuelve los turnos de los enemigos"""
    global combate_activo
    
    if not combate_activo:
        return api_response(False, "No hay combate activo", status_code=400)
    
    resultados = combate_activo.resolver_turno_enemigos()
    
    return api_response(True, "Turnos enemigos resueltos", {"resultados": resultados, "estado": combate_activo.get_estado()})


@combate_bp.route('/estado', methods=['GET'])
def get_estado():
    """Obtiene el estado actual del combate"""
    global combate_activo
    
    if not combate_activo:
        return api_response(False, "No hay combate activo", status_code=400)
    
    return api_response(True, "Estado del combate", combate_activo.get_estado())


@combate_bp.route('/recompensas', methods=['GET'])
def get_recompensas():
    """Obtiene las recompensas del combate ganado"""
    global combate_activo
    
    if not combate_activo:
        return api_response(False, "No hay combate activo", status_code=400)
    
    if combate_activo.estado != EstadoCombate.VICTORIA:
        return api_response(False, "No has ganado el combate", status_code=400)
    
    recompensas = combate_activo.get_recompensas()
    return api_response(True, "Recompensas obtenidas", recompensas)


@combate_bp.route('/finalizar', methods=['POST'])
def finalizar_combate():
    """Finaliza el combate y aplica recompensas"""
    global combate_activo
    
    if not combate_activo:
        return api_response(False, "No hay combate activo", status_code=400)
    
    data = request.get_json()
    slot = data.get('slot', 1)
    
    # Cargar partida
    save_manager = SaveManager()
    datos_juego = save_manager.cargar(slot)
    if not datos_juego:
        return api_response(False, "No se encontró la partida", status_code=404)
    
    personaje = Personaje.from_dict(datos_juego['personaje'])
    
    resultado_final = {"estado": combate_activo.estado.value}
    
    # Aplicar recompensas si ganó
    if combate_activo.estado == EstadoCombate.VICTORIA:
        recompensas = combate_activo.get_recompensas()
        
        # Dar experiencia de nivel
        if recompensas.get('experiencia'):
            personaje.ganar_experiencia(recompensas['experiencia'])
        
        # Dar experiencia de habilidades acumulada
        for hab_nombre, exp_cantidad in combate_activo.exp_acumulada.items():
            personaje.ganar_experiencia_habilidad(hab_nombre, exp_cantidad)
        
        # Dar oro
        if recompensas.get('oro'):
            datos_juego['inventario']['oro'] += recompensas['oro']
        
        # Procesar drops de items
        if recompensas.get('drops'):
            inventario = datos_juego['inventario']
            for drop in recompensas['drops']:
                item_id = drop['item_id']
                cantidad = drop['cantidad']
                
                # Intentar apilar o añadir nuevo
                item_existente = next((i for i in inventario['items'] if i['id'] == item_id), None)
                if item_existente:
                    item_existente['cantidad'] += cantidad
                else:
                    if len(inventario['items']) < inventario['slots_maximos']:
                        inventario['items'].append({
                            "id": item_id,
                            "cantidad": cantidad,
                            "tipo": "material" # Por defecto, a refinar si hay base de datos de items
                        })
        
        # Actualizar HP del personaje
        jugador_participante = combate_activo.jugadores.get('jugador_1')
        if jugador_participante:
            personaje.stats.hp_actual = jugador_participante.hp
        
        resultado_final['recompensas'] = recompensas
    
    elif combate_activo.estado == EstadoCombate.HUIDA:
        # Actualizar HP del personaje
        jugador_participante = combate_activo.jugadores.get('jugador_1')
        if jugador_participante:
            personaje.stats.hp_actual = jugador_participante.hp
    
    elif combate_activo.estado == EstadoCombate.DERROTA:
        # Game over - restaurar HP o manejar de otra forma
        personaje.stats.hp_actual = 1  # Dejar con 1 HP
    
    # Guardar cambios
    datos_juego['personaje'] = personaje.to_dict()
    save_manager.guardar(slot, datos_juego)
    
    # Limpiar combate activo
    combate_activo = None
    
    return api_response(True, "Combate finalizado", resultado_final)


@combate_bp.route('/enemigos-disponibles', methods=['GET'])
def get_enemigos_disponibles():
    """Obtiene la lista de enemigos disponibles por categoría"""
    enemigos_data = cargar_enemigos_data()
    
    # Simplificar la respuesta
    resultado = {}
    for categoria, lista in enemigos_data['enemigos'].items():
        resultado[categoria] = [
            {"id": e['id'], "nombre": e['nombre'], "nivel_sugerido": e.get('nivel', 1)}
            for e in lista
        ]
    
    return api_response(True, "Enemigos disponibles", resultado)
