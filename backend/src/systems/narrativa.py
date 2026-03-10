from typing import List, Dict, Optional, Any
from .tiempo import TimeManager
from .npcs.npc import NPC
from .npcs.memory_index import MemoryIndex
from ..llm.client import LLMClient
from ..llm.prompts import PROMPT_NPC_DIALOGO, PROMPT_SISTEMA_BASE

class NarrativaManager:
    """
    Orquestador narrativo: construye el contexto para el LLM uniendo todos los sistemas.
    Gestiona también el historial de eventos y las consecuencias.
    """

    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self.memory_indexer = MemoryIndex()

    def construir_contexto_npc(self, npc: NPC, jugador_data: Dict, tiempo: TimeManager, rumores_locales: List[Dict]) -> Dict:
        """Une todos los datos necesarios para el prompt de diálogo de un NPC."""
        
        # 1. Obtener memoria indexada del NPC
        contexto_memoria = self.memory_indexer.generar_contexto_memoria(npc)
        
        # 2. Formatear datos del jugador
        stats_jugador = jugador_data.get("personaje", {}).get("stats", {})
        jugador_info = {
            "nombre": jugador_data.get("personaje", {}).get("nombre", "Explorador"),
            "nivel": stats_jugador.get("nivel", 1),
            "hp": f"{stats_jugador.get('hp', 100)}/{stats_jugador.get('hp_max', 100)}",
            "tags": jugador_data.get("progreso", {}).get("tags", [])
        }

        # 3. Construir el diccionario final para el prompt
        return {
            "nombre": npc.nombre,
            "raza": npc.raza,
            "rol": f"{npc.rol_tipo} ({npc.rol_subtipo})",
            "personalidad": ", ".join(npc.personalidad.rasgos),
            "emocion": f"{npc.estado.emocion_actual} (intensidad: {npc.estado.emocion_intensidad})",
            "relacion": f"{npc.relacion_jugador.reputacion_estado} (valor: {npc.relacion_jugador.reputacion_valor})",
            "memoria": contexto_memoria.get("resumen_jugador") or "No hay interacciones previas memorables.",
            "rumores": self._formatear_rumores(rumores_locales),
            "ubicacion": npc.ubicacion.ubicacion_id or "el camino",
            "hora": tiempo.get_formato_hora(),
            "clima": "despejado", # Placeholder hasta integrar sistema de clima
            "jugador": jugador_info
        }

    def generar_dialogo_npc(self, npc: NPC, mensaje_jugador: str, jugador_data: Dict, tiempo: TimeManager, rumores_locales: List[Dict]) -> str:
        """Llama al LLM para generar una respuesta del NPC."""
        
        contexto = self.construir_contexto_npc(npc, jugador_data, tiempo, rumores_locales)
        
        # Rellenar el template del prompt
        prompt = PROMPT_NPC_DIALOGO.format(
            nombre=contexto["nombre"],
            raza=contexto["raza"],
            rol=contexto["rol"],
            personalidad=contexto["personalidad"],
            emocion=contexto["emocion"],
            relacion=contexto["relacion"],
            memoria=contexto["memoria"],
            rumores=contexto["rumores"],
            ubicacion=contexto["ubicacion"],
            hora=contexto["hora"],
            clima=contexto["clima"],
            mensaje=mensaje_jugador
        )

        respuesta = self.llm.generar(prompt, system_prompt=PROMPT_SISTEMA_BASE)
        
        if not respuesta:
            return "PAUSE: El narrador ha perdido el hilo de la historia (LLM no disponible)."
            
        return respuesta

    def _formatear_rumores(self, rumores: List[Dict]) -> str:
        if not rumores:
            return "No hay rumores recientes en esta zona."
        
        lineas = []
        for r in rumores[:3]: # Top 3 rumores
            lineas.append(f"- {r.get('contenido', '...')}")
        return "\n".join(lineas)

    def registrar_evento(self, save_data: Dict, tipo: str, descripcion: str, impacto: Dict = None):
        """Registra un evento en el historial global del save."""
        historial = save_data.get("historial_eventos", [])
        
        evento = {
            "id": f"ev_{len(historial) + 1:03d}",
            "timestamp": save_data.get("tiempo", {}).get("tick_total", 0),
            "tipo": tipo,
            "descripcion": descripcion,
            "impacto": impacto or {}
        }
        
        historial.append(evento)
        save_data["historial_eventos"] = historial
        
        # Aquí se podrían procesar consecuencias inmediatas
        if impacto:
            self._procesar_impacto(save_data, impacto)

    def _procesar_impacto(self, save_data: Dict, impacto: Dict):
        """Aplica cambios al estado del mundo basados en el impacto de un evento."""
        # Ejemplo: {"reputacion": {"faccion_id": -10}, "tags": ["matabestias"]}
        if "tags" in impacto:
            tags = save_data.get("progreso", {}).get("tags", [])
            for tag in impacto["tags"]:
                if tag not in tags:
                    tags.append(tag)
            save_data.setdefault("progreso", {})["tags"] = tags
