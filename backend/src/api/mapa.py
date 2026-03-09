"""
API Endpoints para el sistema de mapa mundial.

Endpoints:
- GET /api/mapa/estado - Obtiene el estado actual del mapa
- GET /api/mapa/visual - Obtiene representación visual del mapa
- POST /api/mapa/mover - Mueve al jugador a una posición
- GET /api/mapa/ubicaciones - Obtiene ubicaciones cercanas
- GET /api/mapa/ubicacion/<id> - Obtiene detalles de una ubicación
- POST /api/mapa/explorar - Explora el tile actual
- GET /api/mapa/cartografia - Obtiene estadísticas de cartografía
- POST /api/mapa/cartografia/mapa - Crea un nuevo mapa
- POST /api/mapa/cartografia/usar - Usa un mapa para revelar información
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any, Optional
import traceback
import logging

from systems.seed import WorldSeed, init_global_seed, get_global_seed
from systems.mapa import (
    MapaMundo, 
    SistemaCartografia, 
    TipoMapa, 
    CalidadMapa,
    TipoUbicacion
)

# Configurar logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


# Blueprint para mapa
mapa_bp = Blueprint('mapa', __name__, url_prefix='/api/mapa')


# Cache de mapas por slot (en producción usar Redis o similar)
_mapas_cache: Dict[int, MapaMundo] = {}
_cartografia_cache: Dict[int, SistemaCartografia] = {}


def get_or_create_mapa(slot_num: int, seed_string: Optional[str] = None, mapa_data: Optional[dict] = None) -> MapaMundo:
    """
    Obtiene o crea el mapa para un slot.
    
    Args:
        slot_num: Número de slot
        seed_string: Semilla opcional
        mapa_data: Datos serializados del mapa (si existe)
    
    Returns:
        Instancia de MapaMundo
    """
    if slot_num in _mapas_cache:
        return _mapas_cache[slot_num]
    
    # Crear semilla
    seed = WorldSeed(seed_string) if seed_string else init_global_seed()
    
    # Crear mapa
    if mapa_data:
        mapa = MapaMundo.from_dict(mapa_data, seed)
    else:
        mapa = MapaMundo(seed=seed)
        mapa.generar_mundo_inicial()
    
    _mapas_cache[slot_num] = mapa
    return mapa


def get_or_create_cartografia(slot_num: int, seed_string: Optional[str] = None, cart_data: Optional[dict] = None) -> SistemaCartografia:
    """
    Obtiene o crea el sistema de cartografía para un slot.
    """
    if slot_num in _cartografia_cache:
        return _cartografia_cache[slot_num]
    
    seed = WorldSeed(seed_string) if seed_string else init_global_seed()
    
    if cart_data:
        cartografia = SistemaCartografia.from_dict(cart_data, seed)
    else:
        cartografia = SistemaCartografia(seed)
    
    _cartografia_cache[slot_num] = cartografia
    return cartografia


@mapa_bp.route('/estado', methods=['GET'])
def obtener_estado():
    """
    Obtiene el estado actual del mapa.
    
    Query params:
        - slot: Número de slot (requerido)
    
    Returns:
        - posicion_jugador: Posición actual
        - ubicacion_actual: ID de ubicación actual (si hay)
        - tiles_explorados: Total de tiles explorados
        - ubicaciones_descubiertas: Ubicaciones descubiertas
        - total_ubicaciones: Total de ubicaciones en el mundo
    """
    try:
        slot_num = request.args.get('slot', type=int)
        
        if not slot_num:
            return jsonify({
                "success": False,
                "message": "Falta el slot"
            }), 400
        
        mapa = get_or_create_mapa(slot_num)
        estado = mapa.get_estado_mapa()
        
        return jsonify({
            "success": True,
            "data": estado
        })
    except Exception as e:
        logger.error(f"Error en obtener_estado: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": f"Error al obtener estado: {str(e)}"
        }), 500


@mapa_bp.route('/visual', methods=['GET'])
def obtener_visual():
    """
    Obtiene una representación visual del mapa MUNDIAL.
    
    Query params:
        - slot: Número de slot (requerido)
        - radio: Radio de visión (default: 10)
    
    Returns:
        - mapa: Matriz de caracteres representando el mapa
        - leyenda: Leyenda de símbolos
    """
    try:
        slot_num = request.args.get('slot', type=int)
        radio = request.args.get('radio', default=10, type=int)
        
        if not slot_num:
            return jsonify({
                "success": False,
                "message": "Falta el slot"
            }), 400
        
        mapa = get_or_create_mapa(slot_num)
        visual = mapa.get_mapa_visual(radio)
        
        return jsonify({
            "success": True,
            "data": {
                "mapa": visual,
                "posicion": list(mapa.posicion_jugador),
                "modo": "mundial",
                "leyenda": {
                    "jugador": "📍",
                    "pueblo": "🏘️",
                    "ciudad": "🏰",
                    "capital": "👑",
                    "mazmorra": "⚔️",
                    "poi": "✨",
                    "descubierto": "·",
                    "no_descubierto": "?"
                }
            }
        })
    except Exception as e:
        logger.error(f"Error en obtener_visual: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": f"Error al obtener visual: {str(e)}"
        }), 500


@mapa_bp.route('/local', methods=['GET'])
def obtener_local():
    """
    Obtiene una representación visual del mapa LOCAL (sub-tiles).
    
    Query params:
        - slot: Número de slot (requerido)
        - radio: Radio de visión (default: 6)
    
    Returns:
        - mapa: Matriz de caracteres representando el mapa local
        - posicion_local: Posición dentro del tile (0-9, 0-9)
        - tile_mundial: Coordenadas del tile mundial actual
    """
    try:
        slot_num = request.args.get('slot', type=int)
        radio = request.args.get('radio', default=6, type=int)
        
        if not slot_num:
            return jsonify({
                "success": False,
                "message": "Falta el slot"
            }), 400
        
        mapa = get_or_create_mapa(slot_num)
        visual = mapa.get_mapa_local_visual(radio)
        
        return jsonify({
            "success": True,
            "data": {
                "mapa": visual,
                "posicion": list(mapa.posicion_local),
                "posicion_mundial": list(mapa.posicion_jugador),
                "modo": "local",
                "escala": "1 tile = 10m"
            }
        })
    except Exception as e:
        logger.error(f"Error en obtener_local: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": f"Error al obtener mapa local: {str(e)}"
        }), 500


@mapa_bp.route('/mover', methods=['POST'])
def mover_jugador():
    """
    Mueve al jugador a una nueva posición MUNDIAL.
    
    Body:
        - slot: Número de slot (requerido)
        - x: Coordenada X destino (tiles de 1km)
        - y: Coordenada Y destino (tiles de 1km)
    
    Returns:
        - posicion_anterior: Posición anterior
        - posicion_nueva: Nueva posición
        - distancia: Distancia recorrida
        - tiempo_horas: Tiempo de viaje
        - tile: Información del tile destino
    """
    try:
        data = request.get_json()
        
        if not data or 'slot' not in data:
            return jsonify({
                "success": False,
                "message": "Falta el slot"
            }), 400
        
        slot_num = data['slot']
        x = data.get('x', 0)
        y = data.get('y', 0)
        
        mapa = get_or_create_mapa(slot_num)
        resultado = mapa.mover_jugador(x, y)
        
        return jsonify({
            "success": True,
            "message": f"Movido a ({x}, {y})",
            "data": resultado
        })
    except Exception as e:
        logger.error(f"Error en mover_jugador: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": f"Error al mover: {str(e)}"
        }), 500


@mapa_bp.route('/mover-local', methods=['POST'])
def mover_jugador_local():
    """
    Mueve al jugador dentro del tile actual (sub-tiles de 10m).
    
    IMPORTANTE: Este movimiento es LOCAL y NO afecta el mapa mundial.
    
    Body:
        - slot: Número de slot (requerido)
        - x: Coordenada X local (0-9)
        - y: Coordenada Y local (0-9)
    
    Returns:
        - posicion_anterior: Posición local anterior
        - posicion_nueva: Nueva posición local
        - distancia: Distancia recorrida en sub-tiles
        - tiempo_minutos: Tiempo de viaje
        - sub_tile: Información del sub-tile destino
    """
    try:
        data = request.get_json()
        
        if not data or 'slot' not in data:
            return jsonify({
                "success": False,
                "message": "Falta el slot"
            }), 400
        
        slot_num = data['slot']
        x = data.get('x', 5)
        y = data.get('y', 5)
        
        mapa = get_or_create_mapa(slot_num)
        resultado = mapa.mover_jugador_local(x, y)
        
        if "error" in resultado:
            return jsonify({
                "success": False,
                "message": resultado["error"]
            }), 400
        
        return jsonify({
            "success": True,
            "message": f"Movido localmente a ({x}, {y})",
            "data": resultado
        })
    except Exception as e:
        logger.error(f"Error en mover_jugador_local: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": f"Error al mover localmente: {str(e)}"
        }), 500


@mapa_bp.route('/ubicaciones', methods=['GET'])
def obtener_ubicaciones():
    """
    Obtiene las ubicaciones cercanas al jugador.
    
    Query params:
        - slot: Número de slot (requerido)
        - radio: Radio de búsqueda (default: 50)
    
    Returns:
        - ubicaciones: Lista de ubicaciones cercanas
    """
    try:
        slot_num = request.args.get('slot', type=int)
        radio = request.args.get('radio', default=50, type=int)
        
        if not slot_num:
            return jsonify({
                "success": False,
                "message": "Falta el slot"
            }), 400
        
        mapa = get_or_create_mapa(slot_num)
        destinos = mapa.get_destinos_cercanos(radio)
        
        return jsonify({
            "success": True,
            "data": {
                "ubicaciones": destinos,
                "total": len(destinos)
            }
        })
    except Exception as e:
        logger.error(f"Error en obtener_ubicaciones: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": f"Error al obtener ubicaciones: {str(e)}"
        }), 500


@mapa_bp.route('/ubicacion/<ubicacion_id>', methods=['GET'])
def obtener_ubicacion(ubicacion_id: str):
    """
    Obtiene detalles de una ubicación específica.
    
    Query params:
        - slot: Número de slot (requerido)
    
    Returns:
        - ubicacion: Detalles de la ubicación
    """
    try:
        slot_num = request.args.get('slot', type=int)
        
        if not slot_num:
            return jsonify({
                "success": False,
                "message": "Falta el slot"
            }), 400
        
        mapa = get_or_create_mapa(slot_num)
        
        if ubicacion_id not in mapa.ubicaciones:
            return jsonify({
                "success": False,
                "message": f"Ubicación no encontrada: {ubicacion_id}"
            }), 404
        
        ubicacion = mapa.ubicaciones[ubicacion_id]
        
        return jsonify({
            "success": True,
            "data": ubicacion.to_dict()
        })
    except Exception as e:
        logger.error(f"Error en obtener_ubicacion: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": f"Error al obtener ubicación: {str(e)}"
        }), 500


@mapa_bp.route('/viajar', methods=['POST'])
def viajar_ubicacion():
    """
    Viaja a una ubicación conocida.
    
    Body:
        - slot: Número de slot (requerido)
        - ubicacion_id: ID de la ubicación destino
    
    Returns:
        - resultado: Información del viaje
    """
    try:
        data = request.get_json()
        
        if not data or 'slot' not in data or 'ubicacion_id' not in data:
            return jsonify({
                "success": False,
                "message": "Faltan datos (slot, ubicacion_id)"
            }), 400
        
        slot_num = data['slot']
        ubicacion_id = data['ubicacion_id']
        
        mapa = get_or_create_mapa(slot_num)
        resultado = mapa.mover_a_ubicacion(ubicacion_id)
        
        if "error" in resultado:
            return jsonify({
                "success": False,
                "message": resultado["error"]
            }), 404
        
        return jsonify({
            "success": True,
            "message": f"Viajado a {resultado['ubicacion']['nombre']}",
            "data": resultado
        })
    except Exception as e:
        logger.error(f"Error en viajar_ubicacion: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": f"Error al viajar: {str(e)}"
        }), 500


@mapa_bp.route('/explorar', methods=['POST'])
def explorar_tile():
    """
    Explora el tile actual del jugador.
    
    Body:
        - slot: Número de slot (requerido)
    
    Returns:
        - tile: Información del tile explorado
        - ubicacion: Ubicación descubierta (si hay)
    """
    try:
        data = request.get_json()
        
        if not data or 'slot' not in data:
            return jsonify({
                "success": False,
                "message": "Falta el slot"
            }), 400
        
        slot_num = data['slot']
        
        mapa = get_or_create_mapa(slot_num)
        resultado = mapa.explorar_tile_actual()
        
        if "error" in resultado:
            return jsonify({
                "success": False,
                "message": resultado["error"]
            }), 404
        
        return jsonify({
            "success": True,
            "message": "Tile explorado",
            "data": resultado
        })
    except Exception as e:
        logger.error(f"Error en explorar_tile: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": f"Error al explorar: {str(e)}"
        }), 500


@mapa_bp.route('/cartografia', methods=['GET'])
def obtener_cartografia():
    """
    Obtiene las estadísticas de cartografía del jugador.
    
    Query params:
        - slot: Número de slot (requerido)
    
    Returns:
        - estadisticas: Estadísticas de cartografía
    """
    try:
        slot_num = request.args.get('slot', type=int)
        
        if not slot_num:
            return jsonify({
                "success": False,
                "message": "Falta el slot"
            }), 400
        
        cartografia = get_or_create_cartografia(slot_num)
        stats = cartografia.get_estadisticas()
        
        return jsonify({
            "success": True,
            "data": stats
        })
    except Exception as e:
        logger.error(f"Error en obtener_cartografia: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": f"Error al obtener cartografía: {str(e)}"
        }), 500


@mapa_bp.route('/cartografia/mapa', methods=['POST'])
def crear_mapa():
    """
    Crea un nuevo mapa de cartografía.
    
    Body:
        - slot: Número de slot (requerido)
        - tipo: Tipo de mapa (regional, local, dungeon, tesoro, antiguo)
        - calidad: Calidad del mapa (borroso, normal, detallado, preciso, maestro)
        - centro_x: Centro X del área
        - centro_y: Centro Y del área
        - radio: Radio de cobertura (opcional)
    
    Returns:
        - mapa: Mapa creado
    """
    try:
        data = request.get_json()
        
        if not data or 'slot' not in data:
            return jsonify({
                "success": False,
                "message": "Falta el slot"
            }), 400
        
        slot_num = data['slot']
        tipo_str = data.get('tipo', 'local')
        calidad_str = data.get('calidad', 'normal')
        centro_x = data.get('centro_x', 0)
        centro_y = data.get('centro_y', 0)
        radio = data.get('radio')
        
        # Convertir strings a enums
        try:
            tipo = TipoMapa(tipo_str)
            calidad = CalidadMapa(calidad_str)
        except ValueError:
            return jsonify({
                "success": False,
                "message": f"Tipo o calidad inválidos: {tipo_str}, {calidad_str}"
            }), 400
        
        cartografia = get_or_create_cartografia(slot_num)
        mapa = cartografia.crear_mapa(tipo, calidad, centro_x, centro_y, radio)
        
        return jsonify({
            "success": True,
            "message": f"Mapa creado: {mapa.nombre}",
            "data": mapa.to_dict()
        })
    except Exception as e:
        logger.error(f"Error en crear_mapa: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": f"Error al crear mapa: {str(e)}"
        }), 500


@mapa_bp.route('/cartografia/usar', methods=['POST'])
def usar_mapa():
    """
    Usa un mapa para revelar información.
    
    Body:
        - slot: Número de slot (requerido)
        - mapa_id: ID del mapa a usar
    
    Returns:
        - resultado: Información revelada
    """
    try:
        data = request.get_json()
        
        if not data or 'slot' not in data or 'mapa_id' not in data:
            return jsonify({
                "success": False,
                "message": "Faltan datos (slot, mapa_id)"
            }), 400
        
        slot_num = data['slot']
        mapa_id = data['mapa_id']
        
        mapa = get_or_create_mapa(slot_num)
        cartografia = get_or_create_cartografia(slot_num)
        
        resultado = cartografia.usar_mapa(mapa_id, mapa)
        
        if "error" in resultado:
            return jsonify({
                "success": False,
                "message": resultado["error"]
            }), 400
        
        return jsonify({
            "success": True,
            "message": "Mapa usado",
            "data": resultado
        })
    except Exception as e:
        logger.error(f"Error en usar_mapa: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": f"Error al usar mapa: {str(e)}"
        }), 500


@mapa_bp.route('/cartografia/mapas', methods=['GET'])
def obtener_mapas():
    """
    Obtiene los mapas disponibles del jugador.
    
    Query params:
        - slot: Número de slot (requerido)
    
    Returns:
        - mapas: Lista de mapas no usados
    """
    try:
        slot_num = request.args.get('slot', type=int)
        
        if not slot_num:
            return jsonify({
                "success": False,
                "message": "Falta el slot"
            }), 400
        
        cartografia = get_or_create_cartografia(slot_num)
        mapas = cartografia.get_mapas_disponibles()
        
        return jsonify({
            "success": True,
            "data": {
                "mapas": [m.to_dict() for m in mapas],
                "total": len(mapas)
            }
        })
    except Exception as e:
        logger.error(f"Error en obtener_mapas: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": f"Error al obtener mapas: {str(e)}"
        }), 500


# Función para registrar el blueprint en la app
def registrar_blueprint(app):
    """Registra el blueprint de mapa en la app Flask."""
    app.register_blueprint(mapa_bp)