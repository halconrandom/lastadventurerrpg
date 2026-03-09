"""
API Endpoints para el sistema de exploracion procedural.

Endpoints:
- POST /api/exploracion/iniciar - Inicia exploracion en una zona
- GET /api/exploracion/zona/<x>/<y> - Obtiene info de una zona
- POST /api/exploracion/explorar - Ejecuta una accion de exploracion
- GET /api/exploracion/clima/<x>/<y> - Obtiene clima actual
- POST /api/exploracion/evento/resolver - Resuelve un evento
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any, Optional
import traceback
import logging

from systems.seed import WorldSeed, init_global_seed, get_global_seed
from systems.biomas import BiomaGenerator
from systems.zonas import Zona, ZonaGenerator
from systems.eventos import EventoGenerator
from systems.clima import ClimaGenerator

# Configurar logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


# Blueprint para exploracion
exploracion_bp = Blueprint('exploracion', __name__, url_prefix='/api/exploracion')


# Cache de zonas generadas (en produccion usar Redis o similar)
_zonas_cache: Dict[str, Zona] = {}


def get_or_create_seed(seed_string: Optional[str] = None) -> WorldSeed:
    """Obtiene o crea la semilla global."""
    if seed_string:
        return WorldSeed(seed_string)
    
    seed = get_global_seed()
    if not seed:
        seed = init_global_seed()
    return seed


def get_zona_cache_key(slot_num: int, x: int, y: int) -> str:
    """Genera key para cache de zona."""
    return f"{slot_num}_{x}_{y}"


@exploracion_bp.route('/iniciar', methods=['POST'])
def iniciar_exploracion():
    """
    Inicia la exploracion en una zona especifica.
    
    Body:
        - slot: Numero de slot
        - x: Coordenada X
        - y: Coordenada Y
        - seed: Semilla opcional (si no se proporciona, usa la global)
    
    Returns:
        - zona: Informacion de la zona generada
        - bioma: Informacion del bioma
        - clima: Clima actual
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
        seed_string = data.get('seed')
        
        # Obtener o crear semilla
        seed = get_or_create_seed(seed_string)
        
        # Generar zona
        zona_gen = ZonaGenerator(seed)
        zona = zona_gen.generar_zona((x, y))
        
        # Generar clima
        clima_gen = ClimaGenerator(seed)
        clima = clima_gen.generar_clima(zona.bioma.key, f"{x}_{y}")
        
        # Obtener ciclo dia/noche (usar hora del juego o default)
        hora = data.get('hora', 12)
        ciclo = clima_gen.get_ciclo_dia_noche(hora)
        
        # Guardar en cache
        cache_key = get_zona_cache_key(slot_num, x, y)
        _zonas_cache[cache_key] = zona
        
        return jsonify({
            "success": True,
            "message": f"Exploracion iniciada en {zona.nombre}",
            "data": {
                "zona": zona.to_dict(),
                "clima": clima.to_dict(),
                "ciclo": ciclo.to_dict(),
                "descripcion": zona.bioma.get_descripcion()
            }
        })
    except Exception as e:
        logger.error(f"Error en iniciar_exploracion: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": f"Error al iniciar exploracion: {str(e)}"
        }), 500


@exploracion_bp.route('/zona/<int:x>/<int:y>', methods=['GET'])
def obtener_zona(x: int, y: int):
    """
    Obtiene informacion de una zona.
    
    Query params:
        - slot: Numero de slot (requerido)
    
    Returns:
        - zona: Informacion de la zona
    """
    slot_num = request.args.get('slot', type=int)
    
    if not slot_num:
        return jsonify({
            "success": False,
            "message": "Falta el slot"
        }), 400
    
    cache_key = get_zona_cache_key(slot_num, x, y)
    
    if cache_key in _zonas_cache:
        zona = _zonas_cache[cache_key]
        return jsonify({
            "success": True,
            "data": zona.to_dict()
        })
    
    # Si no esta en cache, generar
    seed = get_global_seed()
    if not seed:
        seed = init_global_seed()
    
    zona_gen = ZonaGenerator(seed)
    zona = zona_gen.generar_zona((x, y))
    _zonas_cache[cache_key] = zona
    
    return jsonify({
        "success": True,
        "data": zona.to_dict()
    })


@exploracion_bp.route('/explorar', methods=['POST'])
def ejecutar_exploracion():
    """
    Ejecuta una accion de exploracion en la zona actual.
    
    Body:
        - slot: Numero de slot
        - x: Coordenada X
        - y: Coordenada Y
    
    Returns:
        - resultado: Resultado de la exploracion
        - tiles_descubiertos: Tiles descubiertos
        - encuentros: Encuentros generados
        - poi_descubierto: POI descubierto (si hay)
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
        
        cache_key = get_zona_cache_key(slot_num, x, y)
        
        # Obtener zona del cache o generar
        if cache_key in _zonas_cache:
            zona = _zonas_cache[cache_key]
        else:
            seed = get_global_seed() or init_global_seed()
            zona_gen = ZonaGenerator(seed)
            zona = zona_gen.generar_zona((x, y))
            _zonas_cache[cache_key] = zona
        
        # Ejecutar exploracion
        resultado = zona.explorar()
        
        return jsonify({
            "success": True,
            "message": f"Exploracion completada en {zona.nombre}",
            "data": resultado
        })
    except Exception as e:
        logger.error(f"Error en ejecutar_exploracion: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": f"Error al explorar: {str(e)}"
        }), 500


@exploracion_bp.route('/clima/<int:x>/<int:y>', methods=['GET'])
def obtener_clima(x: int, y: int):
    """
    Obtiene el clima actual para una zona.
    
    Query params:
        - slot: Numero de slot
        - bioma: Key del bioma (opcional, si no hay zona en cache)
        - hora: Hora del dia (default: 12)
    
    Returns:
        - clima: Estado del clima
        - ciclo: Ciclo dia/noche
        - efectos: Efectos combinados
    """
    slot_num = request.args.get('slot', type=int)
    bioma_key = request.args.get('bioma', 'bosque_ancestral')
    hora = request.args.get('hora', default=12, type=int)
    
    seed = get_global_seed() or init_global_seed()
    clima_gen = ClimaGenerator(seed)
    
    # Obtener bioma de la zona en cache o usar el proporcionado
    cache_key = get_zona_cache_key(slot_num, x, y) if slot_num else None
    
    if cache_key and cache_key in _zonas_cache:
        bioma_key = _zonas_cache[cache_key].bioma.key
    
    clima = clima_gen.generar_clima(bioma_key, f"{x}_{y}")
    ciclo = clima_gen.get_ciclo_dia_noche(hora)
    efectos = clima_gen.get_efectos_combinados(clima, ciclo)
    
    return jsonify({
        "success": True,
        "data": {
            "clima": clima.to_dict(),
            "ciclo": ciclo.to_dict(),
            "efectos": efectos
        }
    })


@exploracion_bp.route('/evento', methods=['GET'])
def obtener_evento():
    """
    Obtiene un evento aleatorio para la zona actual.
    
    Query params:
        - slot: Numero de slot
        - x: Coordenada X
        - y: Coordenada Y
    
    Returns:
        - evento: Evento generado
    """
    try:
        slot_num = request.args.get('slot', type=int)
        x = request.args.get('x', default=0, type=int)
        y = request.args.get('y', default=0, type=int)
        
        seed = get_global_seed() or init_global_seed()
        evento_gen = EventoGenerator(seed)
        
        # Obtener bioma de la zona
        bioma_key = None
        cache_key = get_zona_cache_key(slot_num, x, y) if slot_num else None
        
        if cache_key and cache_key in _zonas_cache:
            bioma_key = _zonas_cache[cache_key].bioma.key
        
        evento = evento_gen.generar_evento(f"{x}_{y}", bioma_key)
        
        if not evento:
            return jsonify({
                "success": False,
                "message": "No hay eventos disponibles"
            }), 404
        
        return jsonify({
            "success": True,
            "data": evento.to_dict()
        })
    except Exception as e:
        logger.error(f"Error en obtener_evento: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": f"Error al obtener evento: {str(e)}"
        }), 500


@exploracion_bp.route('/evento/resolver', methods=['POST'])
def resolver_evento():
    """
    Resuelve un evento con la opcion elegida.
    
    Body:
        - evento_id: ID del evento
        - opcion: Indice de la opcion elegida
        - contexto: Contexto adicional (opcional)
    
    Returns:
        - resultado: Resultado del evento
    """
    try:
        data = request.get_json()
        
        if not data or 'evento_id' not in data or 'opcion' not in data:
            return jsonify({
                "success": False,
                "message": "Faltan datos (evento_id, opcion)"
            }), 400
        
        evento_id = data['evento_id']
        opcion = data['opcion']
        contexto = data.get('contexto', 'default')
        
        seed = get_global_seed() or init_global_seed()
        evento_gen = EventoGenerator(seed)
        
        evento = evento_gen.get_evento_by_id(evento_id)
        
        if not evento:
            return jsonify({
                "success": False,
                "message": f"Evento no encontrado: {evento_id}"
            }), 404
        
        resultado = evento_gen.resolver_evento(evento, opcion, contexto)
        
        return jsonify({
            "success": True,
            "message": "Evento resuelto",
            "data": resultado
        })
    except Exception as e:
        logger.error(f"Error en resolver_evento: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": f"Error al resolver evento: {str(e)}"
        }), 500


@exploracion_bp.route('/seed', methods=['POST'])
def establecer_seed():
    """
    Establece la semilla global para la partida.
    
    Body:
        - seed: String de semilla (opcional, genera una si no se proporciona)
    
    Returns:
        - seed: Semilla establecida
    """
    data = request.get_json() or {}
    seed_string = data.get('seed')
    
    seed = init_global_seed(seed_string)
    
    return jsonify({
        "success": True,
        "message": "Semilla establecida",
        "data": {
            "seed": str(seed)
        }
    })


@exploracion_bp.route('/seed', methods=['GET'])
def obtener_seed():
    """
    Obtiene la semilla global actual.
    
    Returns:
        - seed: Semilla actual
    """
    seed = get_global_seed()
    
    if not seed:
        return jsonify({
            "success": False,
            "message": "No hay semilla establecida"
        }), 404
    
    return jsonify({
        "success": True,
        "data": {
            "seed": str(seed)
        }
    })


# Funcion para registrar el blueprint en la app
def registrar_blueprint(app):
    """Registra el blueprint de exploracion en la app Flask."""
    app.register_blueprint(exploracion_bp)
