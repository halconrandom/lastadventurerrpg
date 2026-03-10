from typing import List, Dict, Optional, Any
import json
import re
from systems.tiempo import TimeManager
from systems.npcs.npc import NPC
from systems.npcs.memory_index import MemoryIndex
from systems.npcs.intent_parser import IntentParser
from systems.npcs.dialogue_policy import DialoguePolicy
from llm.client import LLMClient
from llm.prompts import PROMPT_NPC_DIALOGO, PROMPT_SISTEMA_BASE

class NarrativaManager:
    """
    Orquestador narrativo: construye el contexto para el LLM y parsea la respuesta.
    """

    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self.memory_indexer = MemoryIndex()
        self.intent_parser = IntentParser(llm_client)
        self.dialogue_policy = DialoguePolicy()

    def generar_dialogo_npc(self, npc: NPC, mensaje_jugador: str, jugador_data: Dict, tiempo: TimeManager, rumores_locales: List[Dict]) -> Dict:
        """Llama al LLM para generar una respuesta estructurada del NPC."""
        
        # 1. Interpretar intención del jugador (NUEVA CAPA)
        intent = self.intent_parser.parsear(mensaje_jugador)
        
        # 2. Obtener memoria indexada del NPC
        contexto_memoria = self.memory_indexer.generar_contexto_memoria(npc)
        
        # 3. Construir el prompt con el análisis de intención
        prompt = PROMPT_NPC_DIALOGO.format(
            nombre=npc.nombre,
            raza=npc.raza,
            rol=f"{npc.rol_tipo} ({npc.rol_subtipo})",
            personalidad=", ".join(npc.personalidad.rasgos),
            perfil_relacion=contexto_memoria["perfil_relacion"],
            animo_valor=npc.relacion_jugador.reputacion_valor,
            hilo_reciente=contexto_memoria["hilo_reciente"],
            mensaje=mensaje_jugador,
            intent_analisis=json.dumps(intent) # Inyectar análisis de intención
        )

        respuesta_raw = self.llm.generar(prompt, system_prompt=PROMPT_SISTEMA_BASE)
        
        if not respuesta_raw:
            return {
                "pensamiento": "Error de conexión",
                "animo_delta": 0,
                "decision": "HABLAR",
                "respuesta": "..."
            }
            
        try:
            # Intentar parsear el JSON del LLM
            inicio = respuesta_raw.find('{')
            fin = respuesta_raw.rfind('}') + 1
            if inicio != -1 and fin != -1:
                respuesta_json = json.loads(respuesta_raw[inicio:fin])
            else:
                respuesta_json = json.loads(respuesta_raw)
                
            # 4. Validar decisión con DialoguePolicy (NUEVA CAPA)
            decision_original = respuesta_json.get("decision", "HABLAR")
            decision_validada = self.dialogue_policy.validar_decision(npc, intent, decision_original)
            respuesta_json["decision"] = decision_validada
            
            # Actualizar el ánimo del NPC en el objeto real
            delta = respuesta_json.get("animo_delta", 0)
            npc.relacion_jugador.reputacion_valor += delta
            
            return respuesta_json

        except (json.JSONDecodeError, ValueError) as e:
            # Fallback si el LLM no devuelve JSON
            respuesta_limpia = respuesta_raw.split("]")[-1].strip() if "]" in respuesta_raw else respuesta_raw
            return {
                "pensamiento": "Fallo en el motor lógico",
                "animo_delta": 0,
                "decision": "HABLAR",
                "respuesta": respuesta_limpia
            }

    def _extraer_etiqueta(self, texto: str, etiqueta: str) -> Optional[str]:
        """Extrae el contenido de una etiqueta tipo [ETIQUETA] contenido."""
        pattern = rf"\[{etiqueta}\]\s*(.*?)(?=\n\[|\Z)"
        match = re.search(pattern, texto, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else None

    def _formatear_rumores(self, rumores: List[Dict]) -> str:
        if not rumores: return "No hay rumores."
        return "\n".join([f"- {r.get('contenido', '...')}" for r in rumores[:3]])
