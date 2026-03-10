from flask import Blueprint, request, jsonify
from systems.save_manager import SaveManager
from systems.npcs.npc_manager import NPCManager
from systems.seed import init_global_seed

npcs_bp = Blueprint('npcs', __name__)
save_manager = SaveManager()

def get_npc_manager(slot_num):
    datos, _ = save_manager.cargar(slot_num)
    if not datos:
        return None, None
    
    seed = init_global_seed(datos.get("exploracion", {}).get("seed"))
    manager = NPCManager(seed)
    manager.cargar_desde_save(datos.get("npcs", {}))
    return manager, datos

@npcs_bp.route('/lista', methods=['GET'])
def listar_npcs():
    slot = request.args.get('slot', type=int)
    ubicacion_id = request.args.get('ubicacion_id')
    
    if not slot:
        return jsonify({"success": False, "message": "Falta slot"}), 400
        
    manager, _ = get_npc_manager(slot)
    if not manager:
        return jsonify({"success": False, "message": "Partida no encontrada"}), 404
        
    if ubicacion_id:
        npcs = manager.get_npcs_en_ubicacion(ubicacion_id)
    else:
        # Por defecto devolver activos
        npcs = [manager.obtener_npc(nid) for nid in manager.npcs_activos_ids]
        
    return jsonify({
        "success": True,
        "data": [npc.to_dict() for npc in npcs if npc]
    })

@npcs_bp.route('/<npc_id>', methods=['GET'])
def detalle_npc(npc_id):
    slot = request.args.get('slot', type=int)
    if not slot:
        return jsonify({"success": False, "message": "Falta slot"}), 400
        
    manager, _ = get_npc_manager(slot)
    npc = manager.obtener_npc(npc_id)
    
    if not npc:
        return jsonify({"success": False, "message": "NPC no encontrado"}), 404
        
    return jsonify({
        "success": True,
        "data": npc.to_dict()
    })

@npcs_bp.route('/<npc_id>/hablar', methods=['POST'])
def hablar_npc(npc_id):
    data = request.get_json()
    slot = data.get('slot')
    mensaje_jugador = data.get('mensaje', '')
    
    if not slot:
        return jsonify({"success": False, "message": "Falta slot"}), 400
        
    manager, datos = get_npc_manager(slot)
    npc = manager.obtener_npc(npc_id)
    
    if not npc:
        return jsonify({"success": False, "message": "NPC no encontrado"}), 404
        
    # Placeholder para integración con LLM
    # Aquí se llamaría al NarrativeManager / LLMClient
    respuesta_texto = f"Hola, soy {npc.nombre}. Por ahora solo puedo decirte esto (LLM en desarrollo)."
    
    return jsonify({
        "success": True,
        "data": {
            "respuesta": respuesta_texto,
            "npc": npc.nombre
        }
    })

@npcs_bp.route('/rumores', methods=['GET'])
def obtener_rumores():
    slot = request.args.get('slot', type=int)
    if not slot:
        return jsonify({"success": False, "message": "Falta slot"}), 400
        
    manager, _ = get_npc_manager(slot)
    return jsonify({
        "success": True,
        "data": manager.rumores
    })
