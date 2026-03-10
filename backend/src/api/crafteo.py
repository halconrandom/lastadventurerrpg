"""
API Endpoints para el sistema de crafteo.

Endpoints:
- GET /api/crafteo/estaciones - Lista de estaciones disponibles
- GET /api/crafteo/recetas/<estacion> - Recetas de una estación
- POST /api/crafteo/craftear - Craftear un item
- POST /api/crafteo/craftear_estacion - Craftear una estación
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any
import logging

from systems.crafteo import gestor_crafteo, TipoEstacion
from systems.items import gestor_items
from systems.inventario import get_gestor

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

crafteo_bp = Blueprint("crafteo", __name__, url_prefix="/api/crafteo")


@crafteo_bp.route("/estaciones", methods=["GET"])
def get_estaciones():
    """
    Obtiene la lista de estaciones disponibles.
    """
    try:
        estaciones = []
        for tipo, estacion in gestor_crafteo.estaciones.items():
            estaciones.append(estacion.to_dict())

        return jsonify({"success": True, "estaciones": estaciones})
    except Exception as e:
        logger.error(f"Error getting estaciones: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@crafteo_bp.route("/recetas/<estacion>", methods=["GET"])
def get_recetas_estacion(estacion: str):
    """
    Obtiene las recetas de una estación específica.
    """
    try:
        tipo = TipoEstacion(estacion)
        recetas = gestor_crafteo.get_recetas_por_estacion(tipo)

        return jsonify({"success": True, "estacion": estacion, "recetas": recetas})
    except ValueError:
        return jsonify(
            {"success": False, "error": f"Estación inválida: {estacion}"}
        ), 400
    except Exception as e:
        logger.error(f"Error getting recetas: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@crafteo_bp.route("/recetas_desbloqueadas", methods=["GET"])
def get_recetas_desbloqueadas():
    """
    Obtiene las recetas disponibles según el nivel de skill.
    """
    nivel = request.args.get("nivel", 1, type=int)

    try:
        recetas = gestor_crafteo.get_recetas_desbloqueadas(nivel)

        return jsonify({"success": True, "nivel_skill": nivel, "recetas": recetas})
    except Exception as e:
        logger.error(f"Error getting recetas: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@crafteo_bp.route("/craftear", methods=["POST"])
def craftear_item():
    """
    Craftea un item usando una receta.
    Body: {"slot": 1, "receta_id": "receta_espada_hierro"}
    """
    data = request.get_json()
    slot = data.get("slot", 1)
    receta_id = data.get("receta_id")

    if not receta_id:
        return jsonify({"success": False, "error": "receta_id requerido"}), 400

    try:
        receta = gestor_crafteo.get_receta(receta_id)
        if not receta:
            return jsonify(
                {"success": False, "error": f"Receta no encontrada: {receta_id}"}
            ), 404

        if not receta.id_item:
            return jsonify(
                {"success": False, "error": "Esta receta no produce un item"}
            ), 400

        gestor_inv = get_gestor(slot)
        if not gestor_inv.inventario:
            gestor_inv.crear_inventario_inicial()

        ok, msg = gestor_crafteo.verificar_materiales(
            receta.materiales, gestor_inv.inventario.to_dict()
        )

        if not ok:
            return jsonify({"success": False, "error": msg}), 400

        gestor_inv.inventario.agregar_item

        gestor_inv.inventario = gestor_crafteo.consumir_materiales(
            receta.materiales, gestor_inv.inventario.to_dict()
        )

        item_instancia = gestor_items.crear_instancia(receta.id_item)
        if not item_instancia:
            return jsonify(
                {
                    "success": False,
                    "error": f"Item template no encontrado: {receta.id_item}",
                }
            ), 500

        ok_add, msg_add = gestor_inv.inventario.agregar_item(item_instancia)
        if not ok_add:
            return jsonify(
                {"success": False, "error": f"Error añadiendo item: {msg_add}"}
            ), 400

        return jsonify(
            {
                "success": True,
                "message": f"Crafteado: {receta.nombre}",
                "item": item_instancia.to_dict(),
                "inventario": gestor_inv.inventario.to_dict(),
            }
        )

    except Exception as e:
        logger.error(f"Error crafteando: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@crafteo_bp.route("/craftear_estacion", methods=["POST"])
def craftear_estacion():
    """
    Craftea una estación de trabajo.
    Body: {"slot": 1, "estacion": "yunque"}
    """
    data = request.get_json()
    slot = data.get("slot", 1)
    estacion_id = data.get("estacion")

    if not estacion_id:
        return jsonify({"success": False, "error": "estacion requerida"}), 400

    try:
        tipo = TipoEstacion(estacion_id)
        estacion = gestor_crafteo.get_estacion(tipo)

        if not estacion:
            return jsonify(
                {"success": False, "error": f"Estación no encontrada: {estacion_id}"}
            ), 404

        if not estacion.recetas_craft:
            return jsonify(
                {"success": False, "error": "Esta estación no tiene receta de crafteo"}
            ), 400

        receta = estacion.recetas_craft[0]

        gestor_inv = get_gestor(slot)
        if not gestor_inv.inventario:
            gestor_inv.crear_inventario_inicial()

        ok, msg = gestor_crafteo.verificar_materiales(
            receta.materiales, gestor_inv.inventario.to_dict()
        )

        if not ok:
            return jsonify({"success": False, "error": msg}), 400

        gestor_inv.inventario = gestor_crafteo.consumir_materiales(
            receta.materiales, gestor_inv.inventario.to_dict()
        )

        return jsonify(
            {
                "success": True,
                "message": f"Crafteado: {estacion.nombre}",
                "estacion": estacion.to_dict(),
                "inventario": gestor_inv.inventario.to_dict(),
            }
        )

    except ValueError:
        return jsonify(
            {"success": False, "error": f"Estación inválida: {estacion_id}"}
        ), 400
    except Exception as e:
        logger.error(f"Error crafteando estación: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


def registrar_blueprint(app):
    """Registra el blueprint en la aplicación Flask."""
    app.register_blueprint(crafteo_bp)
