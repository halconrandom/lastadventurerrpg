"""
API Endpoints para el sistema de inventario.

Endpoints:
- GET /api/inventario - Obtiene inventario completo
- POST /api/inventario/agregar - Añade item por ID
- POST /api/inventario/equipar - Equipa item
- POST /api/inventario/desequipar - Desequipa item
- POST /api/inventario/mover - Mover item entre slots
- POST /api/inventario/usar - Usar consumible
- DELETE /api/inventario/tirar - Tirar item
- POST /api/inventario/favorito - Toggle favorito
- POST /api/inventario/ampliar - Ampliar inventario
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any, Optional
import logging

from systems.inventario import GestorInventario, SLOTS_EQUIPAMIENTO, SLOTS_ALFORJAS_MAX
from systems.items import gestor_items, TipoItem

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

inventario_bp = Blueprint("inventario", __name__, url_prefix="/api/inventario")

_gestores: Dict[int, GestorInventario] = {}


def get_gestor(slot: int) -> GestorInventario:
    """Obtiene o crea el gestor de inventario para un slot."""
    if slot not in _gestores:
        _gestores[slot] = GestorInventario(slot)
    return _gestores[slot]


def init_inventario_from_save(slot: int, save_data: Dict[str, Any]) -> bool:
    """Inicializa el inventario desde los datos guardados."""
    gestor = get_gestor(slot)
    inventario_data = save_data.get("inventario")
    if inventario_data:
        return gestor.cargar_inventario(inventario_data)
    return False


def get_inventario_for_save(slot: int) -> Dict[str, Any]:
    """Obtiene los datos del inventario para guardar."""
    gestor = get_gestor(slot)
    return gestor.guardar_inventario()


@inventario_bp.route("", methods=["GET"])
def get_inventario():
    """
    Obtiene el inventario completo del jugador.
    """
    slot = request.args.get("slot", 1, type=int)

    try:
        gestor = get_gestor(slot)
        if not gestor.inventario:
            gestor.crear_inventario_inicial()

        return jsonify({"success": True, "inventario": gestor.inventario.to_dict()})
    except Exception as e:
        logger.error(f"Error obteniendo inventario: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@inventario_bp.route("/agregar", methods=["POST"])
def agregar_item():
    """
    Añade un item al inventario por su ID de template.
    Body: {"slot": 1, "item_id": "espada_hierro", "cantidad": 1}
    """
    data = request.get_json()
    slot = data.get("slot", 1)
    item_id = data.get("item_id")
    cantidad = data.get("cantidad", 1)

    if not item_id:
        return jsonify({"success": False, "error": "item_id requerido"}), 400

    try:
        gestor = get_gestor(slot)
        if not gestor.inventario:
            gestor.crear_inventario_inicial()

        ok, mensaje = gestor.agregar_item_por_id(item_id, cantidad)
        return jsonify(
            {
                "success": ok,
                "message": mensaje,
                "inventario": gestor.inventario.to_dict() if ok else None,
            }
        )
    except Exception as e:
        logger.error(f"Error añadiendo item: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@inventario_bp.route("/equipar", methods=["POST"])
def equipar_item():
    """
    Equipa un item del inventario.
    Body: {"slot": 1, "indice_alforjas": 0, "slot_equipamiento": "mano_derecha"}
    """
    data = request.get_json()
    slot = data.get("slot", 1)
    indice = data.get("indice_alforjas")
    slot_equip = data.get("slot_equipamiento")

    if indice is None or not slot_equip:
        return jsonify(
            {
                "success": False,
                "error": "indice_alforjas y slot_equipamiento requeridos",
            }
        ), 400

    if slot_equip not in SLOTS_EQUIPAMIENTO:
        return jsonify(
            {
                "success": False,
                "error": f"Slot de equipamiento inválido. Slots válidos: {SLOTS_EQUIPAMIENTO}",
            }
        ), 400

    try:
        gestor = get_gestor(slot)
        if not gestor.inventario:
            return jsonify(
                {"success": False, "error": "Inventario no inicializado"}
            ), 400

        ok, mensaje = gestor.inventario.equipar_item(indice, slot_equip)
        return jsonify(
            {
                "success": ok,
                "message": mensaje,
                "inventario": gestor.inventario.to_dict(),
            }
        )
    except Exception as e:
        logger.error(f"Error equipar item: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@inventario_bp.route("/desequipar", methods=["POST"])
def desequipar_item():
    """
    Desequipa un item y lo mueve al inventario.
    Body: {"slot": 1, "slot_equipamiento": "mano_derecha", "indice_alforjas": 5}
    """
    data = request.get_json()
    slot = data.get("slot", 1)
    slot_equip = data.get("slot_equipamiento")
    indice_alforjas = data.get("indice_alforjas")

    if not slot_equip:
        return jsonify({"success": False, "error": "slot_equipamiento requerido"}), 400

    try:
        gestor = get_gestor(slot)
        if not gestor.inventario:
            return jsonify(
                {"success": False, "error": "Inventario no inicializado"}
            ), 400

        ok, mensaje = gestor.inventario.desequipar_item(slot_equip, indice_alforjas)
        return jsonify(
            {
                "success": ok,
                "message": mensaje,
                "inventario": gestor.inventario.to_dict(),
            }
        )
    except Exception as e:
        logger.error(f"Error desequipar item: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@inventario_bp.route("/mover", methods=["POST"])
def mover_item():
    """
    Mueve un item entre slots.
    Body: {"slot": 1, "origen": "alforjas", "indice_origen": 0, "destino": "alforjas", "indice_destino": 5}
    """
    data = request.get_json()
    slot = data.get("slot", 1)
    origen = data.get("origen")
    indice_origen = data.get("indice_origen")
    destino = data.get("destino")
    indice_destino = data.get("indice_destino")

    if not all(
        [origen, indice_origen is not None, destino, indice_destino is not None]
    ):
        return jsonify(
            {
                "success": False,
                "error": "origen, indice_origen, destino e indice_destino requeridos",
            }
        ), 400

    try:
        gestor = get_gestor(slot)
        if not gestor.inventario:
            return jsonify(
                {"success": False, "error": "Inventario no inicializado"}
            ), 400

        ok, mensaje = gestor.inventario.mover_item(
            origen, indice_origen, destino, indice_destino
        )
        return jsonify(
            {
                "success": ok,
                "message": mensaje,
                "inventario": gestor.inventario.to_dict(),
            }
        )
    except Exception as e:
        logger.error(f"Error mover item: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@inventario_bp.route("/usar", methods=["POST"])
def usar_item():
    """
    Usa un item consumible.
    Body: {"slot": 1, "indice": 0}
    """
    data = request.get_json()
    slot = data.get("slot", 1)
    indice = data.get("indice")

    if indice is None:
        return jsonify({"success": False, "error": "indice requerido"}), 400

    try:
        gestor = get_gestor(slot)
        if not gestor.inventario:
            return jsonify(
                {"success": False, "error": "Inventario no inicializado"}
            ), 400

        ok, mensaje = gestor.inventario.usar_item(indice)
        return jsonify(
            {
                "success": ok,
                "message": mensaje,
                "inventario": gestor.inventario.to_dict() if ok else None,
            }
        )
    except Exception as e:
        logger.error(f"Error usar item: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@inventario_bp.route("/tirar", methods=["DELETE"])
def tirar_item():
    """
    Tira un item del inventario.
    Body: {"slot": 1, "indice": 0}
    """
    data = request.get_json()
    slot = data.get("slot", 1)
    indice = data.get("indice")

    if indice is None:
        return jsonify({"success": False, "error": "indice requerido"}), 400

    try:
        gestor = get_gestor(slot)
        if not gestor.inventario:
            return jsonify(
                {"success": False, "error": "Inventario no inicializado"}
            ), 400

        ok, mensaje = gestor.inventario.tirar_item(indice)
        return jsonify(
            {
                "success": ok,
                "message": mensaje,
                "inventario": gestor.inventario.to_dict() if ok else None,
            }
        )
    except Exception as e:
        logger.error(f"Error tirar item: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@inventario_bp.route("/favorito", methods=["POST"])
def toggle_favorito():
    """
    Marca/desmarca un item como favorito.
    Body: {"slot": 1, "indice": 0}
    """
    data = request.get_json()
    slot = data.get("slot", 1)
    indice = data.get("indice")

    if indice is None:
        return jsonify({"success": False, "error": "indice requerido"}), 400

    try:
        gestor = get_gestor(slot)
        if not gestor.inventario:
            return jsonify(
                {"success": False, "error": "Inventario no inicializado"}
            ), 400

        ok, mensaje = gestor.inventario.toggle_favorito(indice)
        return jsonify(
            {
                "success": ok,
                "message": mensaje,
                "inventario": gestor.inventario.to_dict(),
            }
        )
    except Exception as e:
        logger.error(f"Error toggle favorito: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@inventario_bp.route("/ampliar", methods=["POST"])
def ampliar_inventario():
    """
    Amplía la capacidad del inventario.
    Body: {"slot": 1, "slots": 5}
    """
    data = request.get_json()
    slot = data.get("slot", 1)
    slots = data.get("slots", 2)

    try:
        gestor = get_gestor(slot)
        if not gestor.inventario:
            gestor.crear_inventario_inicial()

        ok, mensaje = gestor.inventario.ampliar_inventario(slots)
        return jsonify(
            {
                "success": ok,
                "message": mensaje,
                "inventario": gestor.inventario.to_dict(),
            }
        )
    except Exception as e:
        logger.error(f"Error ampliar inventario: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@inventario_bp.route("/stats", methods=["GET"])
def get_stats_equipados():
    """
    Obtiene los stats合计 de los items equipados.
    """
    slot = request.args.get("slot", 1, type=int)

    try:
        gestor = get_gestor(slot)
        if not gestor.inventario:
            gestor.crear_inventario_inicial()

        stats = gestor.inventario.get_stats_equipados()
        return jsonify({"success": True, "stats": stats})
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


def registrar_blueprint(app):
    """Registra el blueprint en la aplicación Flask."""
    app.register_blueprint(inventario_bp)
