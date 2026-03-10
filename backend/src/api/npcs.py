from flask import Blueprint, request, jsonify
from systems.save_manager import SaveManager
from systems.npcs.npc_manager import NPCManager
from systems.seed import init_global_seed
from systems.tiempo import TimeManager
from systems.narrativa import NarrativaManager
from llm.client import LLMClient

npcs_bp = Blueprint('npcs', __name__)
save_manager = SaveManager()
llm_client = LLMClient() # Instancia global para la API
narrativa_manager = NarrativaManager(llm_client)

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
        
    manager, datos_partida = get_npc_manager(slot)
    if not manager:
        return jsonify({"success": False, "message": "Partida no encontrada"}), 404
        
    if ubicacion_id:
        npcs = manager.get_npcs_en_ubicacion(ubicacion_id)
    else:
        # Por defecto devolver activos, si no hay activos, devolver los del pueblo de inicio para testeo
        npcs = [manager.obtener_npc(nid) for nid in manager.npcs_activos_ids]
        if not npcs:
            npcs = manager.get_npcs_en_ubicacion("pueblo_inicio")
        
    # Guardar cambios si se generaron NPCs
    datos_partida["npcs"] = manager.to_dict()
    save_manager.guardar(slot, datos_partida)
        
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
        
    # Integración real con NarrativaManager y LLM
    tiempo_dict = datos.get("tiempo", {"tick_total": 480})
    tiempo = TimeManager.from_dict(tiempo_dict)
    rumores = manager.rumores
    
    try:
        respuesta_json = narrativa_manager.generar_dialogo_npc(
            npc=npc,
            mensaje_jugador=mensaje_jugador,
            jugador_data=datos,
            tiempo=tiempo,
            rumores_locales=rumores
        )
        
        if not isinstance(respuesta_json, dict):
            raise ValueError("Respuesta del motor narrativo no es un diccionario")
            
    except Exception as e:
        import traceback
        print(f"ERROR CRÍTICO en narrativa_manager: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            "success": False, 
            "message": f"Error interno en el motor narrativo: {str(e)}"
        }), 500
    
    respuesta_texto = respuesta_json.get("respuesta", "...")
    
    # Registrar la interacción en la memoria del NPC
    interaccion = {
        "jugador": mensaje_jugador,
        "npc": respuesta_texto,
        "timestamp": tiempo.tick_total
    }
    
    # Asegurar que la estructura de memoria existe
    if not hasattr(npc, 'memoria') or npc.memoria is None:
        from systems.npcs.npc import MemoriaNPC
        npc.memoria = MemoriaNPC()
        
    npc.memoria.ultimas_interacciones.append(interaccion)
    
    # Guardar cambios en el NPC y en el save
    datos["npcs"] = manager.to_dict()
    save_manager.guardar(slot, datos)
    
    return jsonify({
        "success": True,
        "data": {
            "respuesta": respuesta_texto,
            "npc": npc.nombre,
            "debug": {
                "pensamiento": respuesta_json.get("pensamiento"),
                "animo_delta": respuesta_json.get("animo_delta"),
                "decision": respuesta_json.get("decision")
            }
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
