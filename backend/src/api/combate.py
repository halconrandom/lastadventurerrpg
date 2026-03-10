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
from systems.mapa import MapaMundo
from systems.seed import WorldSeed

combate_bp = Blueprint('combate', __name__)


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


def get_combate_cache_key(slot: int) -> str:
    """Genera una clave única para el cache de combate por slot"""
    return f"combate_slot_{slot}"


# Cache de combates activos por slot (en producción usar Redis)
_combates_activos = {}  # {slot: CombateManager}


def get_combate_activo(slot: int) -> CombateManager:
    """Obtiene o restaura el combate activo para un slot"""
    cache_key = get_combate_cache_key(slot)
    
    if cache_key in _combates_activos:
        return _combates_activos[cache_key]
    
    # Intentar restaurar desde save
    save_manager = SaveManager()
    datos_juego = save_manager.cargar(slot)
    
    if datos_juego and datos_juego.get("combate"):
        combate_data = datos_juego["combate"]
        combate = CombateManager()
        combate.estado = EstadoCombate(combate_data["estado"])
        combate.turno = combate_data["turno"]
        combate.orden_turnos = combate_data["orden_turnos"]
        combate.indice_turno_actual = combate_data["indice_turno_actual"]
        
        # Restaurar jugadores
        for jid, jdata in combate_data.get("jugadores", {}).items():
            from systems.combate import Participante
            combate.jugadores[jid] = Participante(**jdata)
        
        # Restaurar enemigos
        for eid, edata in combate_data.get("enemigos", {}).items():
            from systems.combate import Participante
            combate.enemigos[eid] = Participante(**edata)
        
        # Restaurar log
        for log_entry in combate_data.get("log", []):
            from systems.combate import EntradaLog
            combate.log.append(EntradaLog(**log_entry))
        
        _combates_activos[cache_key] = combate
        return combate
    
    return None


def guardar_combate_activo(slot: int, combate: CombateManager):
    """Guarda el estado del combate en el savefile"""
    cache_key = get_combate_cache_key(slot)
    _combates_activos[cache_key] = combate
    
    # Guardar en el savefile
    save_manager = SaveManager()
    datos_juego = save_manager.cargar(slot)
    
    if datos_juego:
        datos_juego["combate"] = combate.get_estado()
        save_manager.guardar(slot, datos_juego)


def limpiar_combate_activo(slot: int):
    """Limpia el combate activo del cache y del savefile"""
    cache_key = get_combate_cache_key(slot)
    
    if cache_key in _combates_activos:
        del _combates_activos[cache_key]
    
    # Limpiar del savefile
    save_manager = SaveManager()
    datos_juego = save_manager.cargar(slot)
    
    if datos_juego:
        datos_juego["combate"] = None
        save_manager.guardar(slot, datos_juego)


@combate_bp.route('/iniciar', methods=['POST'])
def iniciar_combate():
    """Inicia un nuevo combate"""
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
    combate = CombateManager()
    estado = combate.iniciar_combate(personaje, enemigos_template)
    
    # Guardar combate activo
    guardar_combate_activo(slot, combate)
    
    return api_response(True, "Combate iniciado", estado)


@combate_bp.route('/accion', methods=['POST'])
def ejecutar_accion():
    """Ejecuta una acción del jugador en combate"""
    data = request.get_json()
    slot = data.get('slot', 1)
    actor_id = data.get('actor_id', 'jugador_1')
    accion = data.get('accion')
    objetivo_id = data.get('objetivo_id')
    habilidad_nombre = data.get('habilidad_nombre')
    item_id = data.get('item_id')

    combate = get_combate_activo(slot)
    if not combate:
        return api_response(False, "No hay combate activo", status_code=400)

    if not accion:
        return api_response(False, "No se especificó acción", status_code=400)

    # Validar acción
    acciones_validas = ["atacar", "habilidad", "item", "bloquear", "evadir", "huir"]
    if accion not in acciones_validas:
        return api_response(False, f"Acción no válida. Acciones válidas: {', '.join(acciones_validas)}", status_code=400)

    resultado = combate.ejecutar_accion(
        actor_id, accion, objetivo_id, habilidad_nombre, item_id
    )

    # Guardar estado actualizado
    guardar_combate_activo(slot, combate)

    return api_response(True, "Acción ejecutada", resultado)


@combate_bp.route('/resolver-enemigos', methods=['POST'])
def resolver_enemigos():
    """Resuelve los turnos de los enemigos"""
    data = request.get_json()
    slot = data.get('slot', 1)
    
    combate = get_combate_activo(slot)
    if not combate:
        return api_response(False, "No hay combate activo", status_code=400)
    
    resultados = combate.resolver_turno_enemigos()
    
    # Guardar estado actualizado
    guardar_combate_activo(slot, combate)
    
    return api_response(True, "Turnos enemigos resueltos", {"resultados": resultados, "estado": combate.get_estado()})


@combate_bp.route('/estado', methods=['GET'])
def get_estado():
    """Obtiene el estado actual del combate"""
    slot = request.args.get('slot', 1, type=int)
    
    combate = get_combate_activo(slot)
    if not combate:
        return api_response(False, "No hay combate activo", status_code=400)
    
    return api_response(True, "Estado del combate", combate.get_estado())


@combate_bp.route('/recompensas', methods=['GET'])
def get_recompensas():
    """Obtiene las recompensas del combate ganado"""
    slot = request.args.get('slot', 1, type=int)
    
    combate = get_combate_activo(slot)
    if not combate:
        return api_response(False, "No hay combate activo", status_code=400)
    
    if combate.estado != EstadoCombate.VICTORIA:
        return api_response(False, "No has ganado el combate", status_code=400)
    
    recompensas = combate.get_recompensas()
    return api_response(True, "Recompensas obtenidas", recompensas)


@combate_bp.route('/finalizar', methods=['POST'])
def finalizar_combate():
    """Finaliza el combate y aplica recompensas"""
    data = request.get_json()
    slot = data.get('slot', 1)
    
    combate = get_combate_activo(slot)
    if not combate:
        return api_response(False, "No hay combate activo", status_code=400)
    
    # Cargar partida
    save_manager = SaveManager()
    datos_juego = save_manager.cargar(slot)
    if not datos_juego:
        return api_response(False, "No se encontró la partida", status_code=404)
    
    personaje = Personaje.from_dict(datos_juego['personaje'])
    
    resultado_final = {"estado": combate.estado.value}
    
    # Aplicar recompensas si ganó
    if combate.estado == EstadoCombate.VICTORIA:
        recompensas = combate.get_recompensas()
        
        # Dar experiencia de nivel
        if recompensas.get('experiencia'):
            personaje.ganar_experiencia(recompensas['experiencia'])
        
        # Dar experiencia de habilidades acumulada
        for hab_nombre, exp_cantidad in combate.exp_acumulada.items():
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
        jugador_participante = combate.jugadores.get('jugador_1')
        if jugador_participante:
            personaje.stats.hp_actual = jugador_participante.hp
        
        # Marcar POI como completado si existe
        mapa_data = datos_juego.get("mapa")
        if mapa_data:
            seed = WorldSeed(mapa_data.get("seed", "default"))
            mapa = MapaMundo.from_dict(mapa_data, seed)
            x, y = mapa.posicion_jugador
            tile = mapa.gestor_chunks.get_tile(x, y)
            if tile and tile.tiene_poi and not tile.poi_completado:
                tile.poi_completado = True
                # Regenerar en 3 días
                tiempo_data = datos_juego.get("tiempo", {"tick_total": 480})
                tile.poi_fecha_regeneracion = tiempo_data["tick_total"] + (24 * 60 * 3)
            datos_juego["mapa"] = mapa.to_dict()
        
        resultado_final['recompensas'] = recompensas
    
    elif combate.estado == EstadoCombate.HUIDA:
        # Actualizar HP del personaje
        jugador_participante = combate.jugadores.get('jugador_1')
        if jugador_participante:
            personaje.stats.hp_actual = jugador_participante.hp
            
        # Fortalecer POI si existe
        mapa_data = datos_juego.get("mapa")
        if mapa_data:
            seed = WorldSeed(mapa_data.get("seed", "default"))
            mapa = MapaMundo.from_dict(mapa_data, seed)
            x, y = mapa.posicion_jugador
            tile = mapa.gestor_chunks.get_tile(x, y)
            if tile and tile.tiene_poi and not tile.poi_completado:
                # Fortalecer: subir nivel
                nivel_actual = tile.poi_data.get("nivel", 1)
                tile.poi_data["nivel"] = nivel_actual + 1
                tile.poi_data["fortificado"] = True
            datos_juego["mapa"] = mapa.to_dict()
    
    elif combate.estado == EstadoCombate.DERROTA:
        # Game over - restaurar HP o manejar de otra forma
        personaje.stats.hp_actual = 1  # Dejar con 1 HP
    
    # Guardar cambios
    datos_juego['personaje'] = personaje.to_dict()
    datos_juego['combate'] = None  # Limpiar combate del save
    save_manager.guardar(slot, datos_juego)
    
    # Limpiar combate activo del cache
    limpiar_combate_activo(slot)
    
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
